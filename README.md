# Presentation on statistics and bioinformatics

I gave a talk on various extensions of the linear statistical model that are used in
some bioinformatics tools for analysing RNA-Seq data on 2019-09-30 to the University
of Glasgow bioinformatics meetup.

If you want to look at the slides see ![here](http://rpubs.com/russH/533927)

If you've cloned this project and want to run it locally:

```
# --- project environment is managed by conda

# create build-matched environment within which to run the project
conda create --name bfx_201909 --file envs/requirements.txt

# OR
# create a less stringently-matching environment,
conda env create --name bfx_201909 --file envs/environment.yml

# ensure the environment is active
conda activate bfx_201909
```

```
# --- filepaths and project-specific stuff are setup by a tool called sidekick that is within the repo
./sidekick setup
```

```
# --- running the project is managed by snakemake
# 
# this will download all relevant data files and any images used in the presentation
# then compile the .Rmd file to an ioslides presentation
snakemake -p
```

You can then view the presentation (`doc/stats_and_bfx.html`) in the browser

When I presented this talk to the U of Glasgow bioinformatics meetup I used a xaringan presentation.
The xaringan version of this talk is still available, but you'll need to pull out release v1.0.0
of the repo and save it locally.

---

# Plan for presentation on statistics and bioinformatics

----

How to structure the presentation?

- Talk or guided conversation

- Focus on:

    - models we use everyday (and might misunderstand)
    
        - can we reimplement limma / edgeR from first principles
        
        - can we extend limma / edgeR using stan|jags / lme4 / Manova

    - novel / nonstandard techniques that lie under the hood of tools we use
    everyday

    - should it be "interesting new stuff" or "understanding the basics"?

----

What topics to include?

- What training is provided for UoG staff / researchers

- What is / is not covered in the MSc

- Tools / resources to improve statistical understanding of collaborators /
  bioinformaticians

- Interesting uses of stats in recent papers / projects

- Compare some basic statistical models / methods using different tools

- Comparative analysis of a dataset using different models

- Local statistical reseearchers / meetups etc

----

What resources to highlight?

Books:

Courses (online):

Courses (UoG):

Courses (external):

Podcasts etc etc:

----

Who (people / groups) to mention?

- RSS Glasgow

- R Users Glasgow / edinbR

- PyData Edinburgh

- Glasgow statistics researchers:
    - https://www.gla.ac.uk/schools/mathematicsstatistics/research/stats/biostats/#/staff
