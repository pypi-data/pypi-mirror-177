
This package allows you to identify competitors based on co-mentions (this could be co-mentions in news articles, social media etc.)

## Examples of How to Calculate Co-Mention-Based Similarity and Categorise Firms

```sh

import compcate.comention as como 

comention_df = como.random_comention_df()
comention_simi_df = como.comention_similarity(comention_df)
comention_group_df = como.community_detection(comention_simi_df)
