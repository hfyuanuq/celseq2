## Overview

This is `celseq2`, a Python framework for generating the UMI count matrix
from [**CEL-Seq2**](https://doi.org/10.1186/s13059-016-0938-8) sequencing data.

## What is `celseq2`, actually?

1. A bioinformatics pipeline which is seamless, parallelized, and easily
extended to run on computing cluster. It reduces the burden of creating work
flow and speeds up data digestion.
2. A list of independent tools which are robust and computational efficient.
Pipeline is not always the need. Package `celseq2` provides a list of versatile
and stand-alone bash commands to address independent tasks, for example,
`count-umi` is able to quantify the UMIs present in the SAM/BAM file of single
cell.

## Install `celseq2`

``` bash
git clone git@gitlab.com:Puriney/celseq2.git
cd celseq2
pip install ./
```

## Quick Start

Running `celseq2` pipeline is easy as 1-2-3, and here is a quick start tutorial
based on an arbitrary example. Suppose user performed CEL-Seq2 and got samples
designed in the way shown as figure below.

![experiment_2plates_1lane](http://i.imgur.com/Vi2cD6e.png)

The user had two biological samples with 8 and 96 cells respectively, which could come
from two time-points, two tissues, or even two labs. Samples were marked with
two different Illumina sequencing barcodes (blue and orange dots), mixed
together, and subsequently sequenced in the same lane, which finally resulted
to 2 FASTQ files.

By running the pipeline of `celseq2` with the them, the users would get
UMI count matrix for each of the two plates.

### Step-1: Specify Configuration of Workflow

Run `new-configuration-file` command to initiate configuration file (YAML
format), which specifies the details of CEL-Seq2 techniques the users perform,
e.g. the cell barcodes sequence dictionary, and transcriptome annotation
information for quantifying UMIs, etc.

This configuration can be shared and used more than once as long as user is
running pipeline on same specie.

``` bash
new-configuration-file -o /path/to/wonderful_CEL-Seq2_config.yaml
```

Example of configuration is [here](https://gitlab.com/Puriney/celseq2/blob/master/example/config.yaml).

Example of cell barcodes sequence dictionary is [here](https://gitlab.com/Puriney/celseq2/blob/master/example/barcodes_cel-seq_umis96.tab)

### Step-2: Define Experiment Table

Run `new-experiment-table` command to initiate table (space/tab separated
file format) specifying the experiment layout.

``` bash
new-experiment-table -o /path/to/wonderful_experiment_table.txt
```

Fill information into the generated experiment table file.

:warning: Note: column names are NOT allowed to be modified.

:warning: Note: each slot cannot contain any space.

The content of experiment table in this example could be:

| SAMPLE_NAME               | CELL_BARCODES_INDEX   | R1                        | R2                        |
|-----------------------    |---------------------  |-------------------------  |-------------------------  |
| wonderful_experiment1     | 1,8,2-7               | path/to/sampleX-lane2-R1.fastq.gz   | path/to/sampleX-lane2-R2.fastq.gz   |
| wonderful_experiment2     | 1-96                  | path/to/sampleY-lane2-R1.fastq.gz   | path/to/sampleY-lane2-R2.fastq.gz   |

Each row records one pair of FASTQ reads.

To ease the pain of manually specifying `CELL_BARCODES_INDEX`, `celseq2`
recognizes human inputs in various way. Examples of specification of barcodes
indexed from 1 to 8 that present in experiment-1 are listed and are all allowed.

1. `1-8`: the most straightforward way.
2. `1,8,2-7` or `1,8,7-2`: combination of individual and range assignment.
3. `8,1,7-2,6`: redundancy is tolerant.

Read [Experiment Table Specification](https://gitlab.com/Puriney/celseq2/wikis/Examples) for further details when more complexed
experiment design happens.

### Step-3: Run Pipeline of `celseq2`

Examine how many tasks to be performed before actually executing the pipeline:

``` bash
celseq2 --config-file /path/to/wonderful_CEL-Seq2_config.yaml \
    --experiment-table /path/to/wonderful_experiment_table.txt \
    --output-dir /path/to/result_dir \
    --dryrun
```

Launch pipeline in the computing node which performs 10 tasks in parallel.

``` bash
celseq2 --config-file /path/to/wonderful_CEL-Seq2_config.yaml \
    --experiment-table /path/to/wonderful_experiment_table.txt \
    --output-dir /path/to/result_dir \
    -j 10
```

Alternatively, it is straightforward to run the pipeline of `celseq2` by
submitting jobs to cluster, as `celseq2` is built on top of `snakemake` which is
a powerful workflow management framework. For example, in login node on server,
user could run the following command to submit jobs to computing nodes. Here it
submits 10 jobs in parallel with 50G of memory requested by each.

``` bash
celseq2 --config-file /path/to/wonderful_CEL-Seq2_config.yaml \
    --experiment-table /path/to/wonderful_experiment_table.txt \
    --output-dir /path/to/result_dir \
    -j 10 \
    --cluster "qsub -cwd -j y -l h_vmem=50G" &
```

## Result
All the results are saved under <kbd>/path/to/result_dir</kbd> user specified,
which has folder structure:

```
├── annotation
├── expr                    # <== Here is the UMI count matrix
├── input
├── small_diagnose
├── small_fq
├── small_log
├── small_sam
├── small_umi_count
└── small_umi_set
```

In particular, **UMI count matrix** for each of the experiments is
saved in both CSV and HDF5 format and exported to <kbd>expr/</kbd> folder.

```
expr/
├── wonderful_experiment1
│   ├── expr.csv            # <== UMI count matrix (CSV format) for blue plate
│   ├── expr.h5
│   └── item-1
│       ├── expr.csv
│       └── expr.h5
└── wonderful_experiment2
    ├── expr.csv            # <== UMI count matrix (CSV format) for orange plate
    ├── expr.h5
    └── item-2
        ├── expr.csv
        └── expr.h5
```

Results of <kbd>item-X</kbd> are useful when user has FASTQ files from multiple
lanes, or technical/biological replicates. Read [Real Example](https://gitlab.com/Puriney/celseq2/wikis/Examples) for further
details about how to specify experiment table and fetch results when more
complexed (or real) experiment design happens.


## Storage management

To reduce the storage of project, it is suggested to get rid of intermediate
files, in particular FASTQ and SAM files.

Remove generated FASTQ and SAM files:

```
celseq2 --config-file /path/to/wonderful_CEL-Seq2_config.yaml \
    --experiment-table /path/to/wonderful_experiment_table.txt \
    --output-dir /path/to/result_dir \
    -j 10 clean_FQ_SAM
```

Alternatively, user can gzip FASTQ and perform SAM2BAM:

```
celseq2-slim --project-dir /path/to/result_dir -n
celseq2-slim --project-dir /path/to/result_dir
```