# Comparative genomics reveal signatures of ecological specialization in the striped ambrosia beetle Trypodendron lineatum

Authors: Zaide Montes-Ortiz, Dan Dan Zhang, Daniel Powell, Heiko Vogel, Christer Lofstedt, Martin N. Andersson

Journal: BMC Genomics, Volume 27, article number 549 (2026). Published 16 June 2026.
DOI: 10.1186/s12864-026-13049-3
Open access, Creative Commons license.

## Abstract

Background: Beetles (Coleoptera) display exceptional dietary diversity and occupy a wide range of ecological niches, often involving close associations with plants and microbes. Ambrosia beetles (Curculionidae; Scolytinae and Platypodinae) exemplify ecological specialization by cultivating mutualistic fungi within galleries excavated in their host trees' xylem, with the fungi serving as their main food source. The striped ambrosia beetle Trypodendron lineatum is a pest of conifers, relying on its nutritional mutualist Phialophoropsis ferruginea for survival. This fungiculture-based lifestyle provides a system for exploring how specialized mutualism is reflected at the genomic level. We performed a comparative genomics analysis between T. lineatum and nine other beetle species with different ecological specializations, hypothesizing that fungiculture is associated with specific genomic adaptations, including changes in gene family composition related to nutrition, detoxification, and immunity.

Results: The small genome of T. lineatum (74.4 to 83.6 Mb) exhibits comparatively low levels of repetitive DNA (19.9%), including a reduced proportion of transposable elements. Annotation generated 14,830 high-quality gene predictions, most supported by transcript evidence or functional domains. Comparative orthology analysis across ten beetle species identified 13,896 orthogroups, with T. lineatum having 78 species-specific orthogroups comprising 238 genes. Gene family evolution analyses revealed 33 families with significant size changes in T. lineatum, including 16 expansions and 17 contractions. Gene families associated with digestion, detoxification, and immunity were contracted, including glycoside hydrolase 28, cytochrome P450, serpin, and trypsin families. Expansions were found in the THAP and CD80-like immunoglobulin domain families.

Conclusions: The genome of T. lineatum is characterized by low repeat content and compact gene architecture. The observed contractions in key gene families involved in plant digestion, detoxification, and immunity may represent genomic signatures of its obligate mutualistic specialization and narrow ecological niche. These findings provide the first insights into the genomic adaptations of fungus-farming ambrosia beetles, suggesting that co-evolved insect-microbe mutualisms may lead to reductions in a variety of gene families.

## Introduction

Beetles (Coleoptera) comprise over 380,000 described species, and their evolutionary success has been attributed in part to their remarkable diversity of feeding strategies. Bark and ambrosia beetles (family Curculionidae) are both members of subfamily Scolytinae, but differ in feeding behavior, larval development, and associations with symbiotic microbes. Bark beetles feed on host tree phloem inoculated with symbiotic fungi, with larvae constructing individual tunnels. Ambrosia beetles bore into the xylem and cultivate obligate mutualistic fungi within their galleries, relying on these fungal gardens as their sole nutritional source.

Trypodendron lineatum is a significant pest of Holarctic conifer forests. It bores into xylem to establish larval galleries inoculated with spores of its obligate fungal mutualist, Phialophoropsis ferruginea. The beetle finds host trees using volatile organic compounds such as alpha-pinene and ethanol, and uses the female-produced aggregation pheromone lineatin.

A previous study (Biswas et al. 2024) showed that T. lineatum has a reduced repertoire of chemoreceptor-coding genes compared to other scolytine beetles. This study extends that work by asking whether specialization has had broader impacts on other gene families involved in digestion, detoxification, immunity, or development, through a comparative genomic and orthology analysis of T. lineatum and nine other beetle species.

## Methods

### Data sources
The T. lineatum genome assembly was previously published (Biswas et al. 2024) and retrieved from the European Nucleotide Archive (ENA; accession PRJEB74033). Three datasets were used: (1) 13 additional beetle genomes from GenBank/NCBI, (2) annotated proteins from RefSeq for ten beetle species selected for orthology inference, and (3) whole-body transcriptomes of T. lineatum generated in this study plus an existing antennae transcriptome (NCBI PRJNA1126204).

### Genome size estimation and telomeres
Genome size was estimated using a k-mer-based approach: Trimmomatic for quality control, Jellyfish for k-mer frequency analysis (k=21), and GenomeScope 2.0 to determine genome size, heterozygosity, and repeat content. QUAST was used to compare against 13 other beetle genomes. Telomeric regions were searched using tidk and FindTelomer.py, looking for motifs TTAGG, TTAGGG, CCCTAA, and TCAGG.

### Transcriptome sequencing
Adult T. lineatum males and females were collected from a conifer forest in Tagarod, South Sweden, in May 2023 using pheromone-baited traps. Whole bodies of six females and six males (two samples) were used for RNA isolation, library construction (Illumina TrueSeq stranded mRNA), and sequencing on a NovaSeq6000. Reads were quality-filtered with Trimmomatic, mapped with HISAT2, and assembled de novo with Trinity. CD-HIT-EST reduced redundancy, and TransDecoder predicted coding regions.

### Genome annotation
The genome was annotated using two complementary pipelines: MAKER and BRAKER3. Repetitive elements were identified with RepeatModeler and masked with RepeatMasker. MAKER was run in four iterative rounds, incorporating transcriptome evidence, protein sets from nine coleopteran species plus Drosophila melanogaster, and the Insecta_Odb10 BUSCO database. AUGUSTUS and SNAP were trained on round-one gene models. BRAKER3 was run in parallel using RNA-seq and protein evidence, and its output was supplied to MAKER as external gene models in the fourth round. CD-HIT removed redundant sequences (identity threshold 0.98). Annotation quality was assessed with BUSCO (v6, Insecta_Odb10 database) and Annotation Edit Distance (AED).

### Functional annotation and orthology
InterProScan (v5.62-94.0) assigned functional categories using Gene3D, ProSite, Patterns, PANTHER, CDD, Pfam, Phobius, SUPERFAMILY, and TMHMM databases. eggNOG-mapper assigned Gene Ontology terms. Orthology inference used OrthoFinder (v2.5.2) across ten beetle species: T. lineatum, Ips typographus, Dendroctonus ponderosae, Hypothenemus hampei, Tribolium castaneum, Anoplophora glabripennis, Callosobruchus maculatus, Leptinotarsa decemlineata, Diabrotica virgifera, and Aethina tumida. OrthoVenn3 was used for visualization. Orthogroup functions were assigned via InterProScan and BLAST against the NCBI non-redundant insect protein database.

### Gene family evolution
CAFE (v5) was used with the 13,896 orthogroups to estimate gene turnover rates, infer ancestral gene counts, and estimate gene gain/loss rates under a stochastic birth-and-death model. Statistical significance used a threshold of p < 0.05. A species tree was built with IQ-TREE (v2.4.0) using ModelFinder for model selection and 1,000 bootstrap iterations, calibrated with TimeTree5 divergence estimates for T. castaneum and I. typographus.

### Phylogenetic trees
For each significantly contracted or expanded gene family, unrooted phylogenetic trees were reconstructed using IQ-TREE and visualized with iTOL (v.7).

## Results and Discussion

### Genome size and telomeres
Estimated genome size ranged from 74.44 to 83.62 Mb, smaller than most other beetle species. Heterozygosity was estimated at 5.58 to 7.61%. The T. lineatum N50 value (915 kb) is lower than most other beetle assemblies. Telomeric repeats were not detected, likely due to technical limitations in assembling repetitive sequences.

### Annotation quality
Repeat annotation found 19.92% of the genome was repetitive DNA: 14.82% interspersed repeats (3.80% retroelements, mostly LTRs at 3.69%; 2.71% DNA transposons; 0.26% rolling-circle elements), 8.31% unclassified repeats, 3.99% simple repeats, 0.79% low-complexity regions. This is lower transposable element content than D. ponderosae (21.12%), D. valens (45.22%), and T. castaneum (28.90%).

The AED distribution improved across rounds: models with strong evidence support (AED <= 0.3) increased from 64.0% in Round 1 to 67.0% in Round 4. BUSCO analysis (insecta_odb10, n=1367) found 95.2% complete genes (93.1% single-copy, 2.1% duplicated), 1.9% missing, 2.9% fragmented. MAKER identified 15,009 raw genes; after CD-HIT redundancy filtering (186 identical entries removed), the final set was 14,830 non-redundant protein sequences. Of these, 11,551 (76.9%) received at least one functional domain or GO term. A reciprocal BLASTP comparison against the previously published chemoreceptor catalogue (Biswas et al. 2024) recovered 109 of 140 chemoreceptor sequences (77.9%) as high-quality orthologs.

Gene count (14,830) is comparable to D. ponderosae (14,342) and Hycleus cichorii (13,813). Gene architecture analysis showed an average of 6.33 exons per gene, average exon length of 211 bp (shorter than all other species studied), and average intron length of 322 bp (an order of magnitude smaller than A. glabripennis at 3,214 bp and D. virgifera at 10,348 bp). This indicates a particularly compact gene architecture.

### Orthology and gene families
13,896 orthogroups were identified, encompassing 93.5% of predicted genes across all ten species. In T. lineatum, 11,986 of 14,830 genes (80.8%) were assigned to orthogroups; 2,844 remained unassigned, and these were significantly shorter (median 77 amino acids) than assigned genes (385 amino acids), suggesting the unassigned fraction is dominated by fragmentary gene models rather than lineage-specific innovation.

T. lineatum shares the most orthogroups with H. hampei (8,694) and the fewest with C. maculatus (3,716). OrthoFinder identified 78 T. lineatum-specific orthogroups (238 genes total). Functional annotation of these was sparse (18.4% had an InterProScan domain, 7.5% a GO term). A significant enrichment was found for digestive serine proteases (five genes with serine-type endopeptidase activity and the Trypsin Pfam domain, FDR = 9.0e-3). Two enriched Pfam domains of unknown function (DUF4806 and DUF5641, FDR <= 5.8e-3) are candidates for future characterization.

33 gene families showed significant size changes (p <= 0.05) in T. lineatum: 16 expanded, 17 contracted.

Key contracted families:
- Glycoside hydrolase family 28 (GH28, PF00295), encoding plant cell wall degrading enzymes (p = 0.05). This family is typically expanded in herbivorous beetles (D. virgifera, L. decemlineata, A. glabripennis, I. typographus). Its contraction in T. lineatum may reflect that the beetles bore into xylem but feed on fungus rather than digesting plant cell walls directly.
- Cytochrome P450 (PF00067) (p = 0.0066), associated with detoxification and insecticide resistance. Contrasts with expansions reported in A. tumida (116 genes, notable CYP3/CYP4 expansions) and H. hampei. Suggests reduced exposure to diverse plant secondary metabolites due to the fungus-associated lifestyle.
- Serpin (PF00079) (p = 0.037), major inhibitors of immune protease cascades including Toll signaling and melanization. Only a single copy retained in T. lineatum. A similar contraction was found in I. typographus. May reflect immune fine-tuning to tolerate the obligate fungal mutualist, similar to the pea aphid and its Buchnera symbiont.
- Trypsin (PF00089/IPR001254), close to significant contraction (p = 0.052). Trypsins are digestive serine proteases and regulators of immunity and development, including prophenoloxidase-activating factors. Notably, a small T. lineatum-specific expansion of trypsin genes was also found among the species-specific orthogroups, a contrast worth noting in questions about this family. Marked expansions were found in D. virgifera, A. glabripennis, and A. tumida.

Key expanded families:
- THAP domain (PF05485) (p = 0.0003), a DNA-binding transcription factor domain often linked to transposable element activity (P-element superfamily). Notable because T. lineatum has low overall repeat content, making this expansion an interesting contrast. Expansions of TE-associated domains may reflect episodic bursts of transposition rather than classical gradual gene family evolution, so CAFE significance for this family should be interpreted cautiously.
- CD80-like C2-set immunoglobulin domain (PF08205) (p = 0.003), involved in cell-cell recognition, adhesion, and immune signaling. Hypothesized to provide molecular diversity for immune discrimination, allowing the beetle to distinguish its fungal mutualist from pathogens. Illustrated in Figure 2 with a phylogenetic tree of orthogroup OG0000184 (77 sequences across the ten beetle species).

## Conclusions

The comparative genomic analysis reveals distinct genomic signatures reflecting the specialized, obligate nutritional mutualism between T. lineatum and P. ferruginea. A small genome, reduced transposable element content, and compact gene architecture (short introns) distinguish T. lineatum from other beetles. This genomic streamlining may be a specialized adaptation to its fungus-cultivating niche, contrasting with polyphagous or herbivorous beetles facing wider environmental challenges.

The contraction of GH28 may reflect the evolutionary shift from herbivory to fungivory. The contractions of cytochrome P450, serpin, and trypsin gene families suggest a trade-off between broad-spectrum metabolic and immune defense capabilities and the requirements of symbiotic tolerance. This reduction in immune-related gene families may be a key mechanism enabling the beetle to maintain its relationship with its obligate fungal mutualist.

The study suggests that co-evolutionary relationships with microbial mutualists may lead to a reorganization of the insect genome, characterized not by acquisition of new defenses but by loss or reduction of gene families no longer essential for survival, a genomic "pruning" that may reduce the metabolic cost of maintaining unnecessary physiological systems.

## Data availability

Genome sequence data was previously deposited in ENA (accession PRJEB74033). The Whole Genome Shotgun project is at GenBank under accession GCA_055532135.1. All datasets generated in this study are on Figshare (https://doi.org/10.6084/m9.figshare.30692345). RNAseq reads are in SRA under PRJNA1370798. All scripts and the reproducible workflow are on GitHub at https://github.com/lachemontes/comparativeGenomics_Tlin/blob/main/Manual/GuideYou.md.

## Key abbreviations

AED: Annotation Edit Distance. AMP: Antimicrobial peptide. CYP: Cytochrome P450. GH28: Glycoside Hydrolase Family 28. HGT: Horizontal gene transfer. Ig: Immunoglobulin. Imd: Immune deficiency pathway. LTR: Long terminal repeat. NF-kB: Nuclear factor kappa-B. PCWDE: Plant cell wall-degrading enzyme. PG: Polygalacturonase. PPO: Prophenoloxidase. PPAF: Prophenoloxidase-activating factor. TE: Transposable element. THAP: Thanatos-associated protein domain. VOC: Volatile organic compound.

## Note on scope for defense preparation

This knowledge base covers the paper's abstract, introduction, methods, results, discussion, and conclusions. It does not include the full reference list, table contents beyond what is described in text, or supplementary file details beyond what is summarized above. For committee questions about specific citation details, supplementary tables, or exact figures, consult the original paper and its additional files directly.
