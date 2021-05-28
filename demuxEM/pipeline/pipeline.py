import numpy as np
import pegasusio as io

import logging
logger = logging.getLogger(__name__)

from demuxEM.tools import *



def run_pipeline(input_rna_file, input_hto_file, output_name, **kwargs):
    # load input rna data
    data = io.read_input(input_rna_file, genome=kwargs["genome"], modality="rna")
    data.subset_data(modality_subset=['rna'])
    data.concat_data() # in case of multi-organism mixing data
    genome = data.uns["genome"]

    # load input hashing data
    data.update(io.read_input(input_hto_file, genome=genome, modality="hashing"))

    # Extract rna and hashing data
    rna_data = data.get_data(modality="rna")
    hashing_data = data.get_data(modality="hashing")

    # Filter the RNA matrix
    rna_data.obs["n_genes"] = rna_data.X.getnnz(axis=1)
    rna_data.obs["n_counts"] = rna_data.X.sum(axis=1).A1
    obs_index = np.logical_and.reduce(
        (
            rna_data.obs["n_genes"] >= kwargs["min_num_genes"],
            rna_data.obs["n_counts"] >= kwargs["min_num_umis"],
        )
    )
    rna_data._inplace_subset_obs(obs_index)

    # run demuxEM
    estimate_background_probs(hashing_data, random_state=kwargs["random_state"])

    demultiplex(
        rna_data,
        hashing_data,
        min_signal=kwargs["min_signal"],
        alpha=kwargs["alpha"],
        n_threads=kwargs["n_jobs"],
    )

    # annotate raw matrix with demuxEM results
    demux_results = attach_demux_results(input_rna_file, rna_data)

    # generate plots
    if kwargs["gen_plots"]:
        plot_hto_hist(
            hashing_data, "hto_type", output_name + ".ambient_hashtag.hist.pdf", alpha=1.0
        )
        plot_bar(
            hashing_data.uns["background_probs"],
            hashing_data.var_names,
            "Sample ID",
            "Background probability",
            output_name + ".background_probabilities.bar.pdf",
        )
        plot_hto_hist(
            hashing_data, "rna_type", output_name + ".real_content.hist.pdf", alpha=0.5
        )
        plot_rna_hist(rna_data, hashing_data, output_name + ".rna_demux.hist.pdf")
        logger.info("Diagnostic plots are generated.")

    if len(kwargs["gen_gender_plot"]) > 0:
        rna_data.matrices["raw.X"] = rna_data.X.copy()
        rna_data.as_float()
        scale = 1e5 / rna_data.X.sum(axis=1).A1
        rna_data.X.data *= np.repeat(scale, np.diff(data.X.indptr))
        rna_data.X.data = np.log1p(rna_data.X.data)

        for gene_name in kwargs["gen_gender_plot"]:
            plot_gene_violin(
                rna_data,
                gene_name,
                "{output_name}.{gene_name}.violin.pdf".format(
                    output_name=output_name, gene_name=gene_name
                ),
                title="{gene_name}: a gender-specific gene".format(gene_name=gene_name),
            )

        logger.info("Gender-specific gene expression violin plots are generated.")

    # output results
    io.write_output(demux_results, output_name + "_demux.zarr.zip")
    io.write_output(data, output_name + ".out.demuxEM.zarr.zip")

    # output summary statistics
    print("\nSummary statistics:")
    print("total\t{}".format(rna_data.shape[0]))
    for name, value in rna_data.obs["demux_type"].value_counts().iteritems():
        print("{}\t{}".format(name, value))
