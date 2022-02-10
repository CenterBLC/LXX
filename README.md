[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5807148.svg)](https://doi.org/10.5281/zenodo.5807148)  [![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)
# LXX
This repository contains the Rahlfs' LXX edition from 1935 with new features developed by the CBLC. The data is present in the TextFabric format. As a direct source for the CBLC version of RLXX1935 we have used Eliran Wong’s work on the RLXX1935 (https://github.com/eliranwong/LXX-Rahlfs-1935). His work is based on the data available at the Computer Assisted Tools for Septuagint Studies (CATSS) at the University of Pennsylvania (http://ccat.sas.upenn.edu/gopher/text/religion/biblical/lxxmorph). We have converted the material into the TextFabric format (see https://github.com/CenterBLC/NA/tree/main/programs). This allows TF users to access the RLXX1935 text in a convenient way and query it.
# Added Features
The CBLC version of the RLXX1935 version has been enriched with several new features. We have split up the morphological coding into its proper own feature sets like person, number, gender, tense, part of speech, etc. In addition, we have created an alphabetic ordering of all lexemes. Also, word frequency information has been added. This helps instructors of Greek to develop vocab lists in alphabetic order for students. Also, we have added the Greek dictionary entry forms and English as found in the BibleOL (https://bibleol.3bmoodle.dk/). For licenses, please consult https://github.com/EzerIT/BibleOL. Finally, sentence divisions have been added. However, these divisions are simply based on the punctuation found in the Greek text. How the additional features we added were produced is documented in the feature production notebook (https://github.com/CenterBLC/LXX/tree/main/programs)
# What’s next?
The CBLC version of the RLXX1935 version is still a work in progress. On the morphological level, we plan to identify verbal and nominal classes (-ω verbs, -µι, a-declination, o-declination, etc.) and build additional feature sets for them. We also plan to match the strong numbers of the RLXX1935 with the corresponding strong numbers of the BHSa. In this way we hope support comparative studies of Hebrew-Greek valence.
# Why?
Text-Fabric has proven to be an excellent linguistic research tool as it can use richly annotated databases and integrates well into the python/pandas tools for data analysis. Since, except for the Tischendorf Text, Biblical Greek texts did not yet exist as TF apps, CBLC saw the need to make the Greek NT and the Greek text of the OT available as TF apps. In this way we can carry out linguistic research within the TF environment on the Septuagint Greek text and Koine Greek of the NT. Particularly valence analysis of Greek verbs will become possible. Also, valence comparison between Greek and Hebrew words can be carried out.
# How to get started?
Run in a jupyter notebook the following command:
```phython
from tf.fabric import Fabric
from tf.app import use
LXX = use("CenterBLC/LXX", version="1935")
```

