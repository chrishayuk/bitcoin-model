## Blocks dataset
The following table describes the columns of the blocks dataset

| Column Name         | Description |
|---------------------|-------------|
| **Block ID**        | A unique identifier for each block. |
| **hash**            | The cryptographic hash of the block. |
| **time**            | The timestamp of when the block was mined or added to the blockchain. |
| **median_time**     | The median timestamp of the last 11 blocks. Helps prevent timestamp manipulation by miners. |
| **size**            | The size of the block in bytes. |
| **stripped_size**   | The size of the block after removing witness data, in bytes. Relevant for SegWit-enabled blocks. |
| **weight**          | A measure introduced with SegWit to limit block size, calculated based on various block components. |
| **version**         | The block version number indicating the set of block validation rules to follow. |
| **version_hex**     | Hexadecimal representation of the block version. |
| **version_bits**    | Binary/bitwise representation of the block version. |
| **merkle_root**     | The root of the Merkle tree of all transactions in the block. |
| **nonce**           | A value that miners adjust in their effort to produce a hash below the target difficulty. |
| **bits**            | A compact representation of the target difficulty for the block's hash. |
| **difficulty**      | The proof-of-work algorithm difficulty target for the block. |
| **chainwork**       | Cumulative proof-of-work of the blockchain up to this block. |
| **coinbase_data_hex** | Data from the coinbase transaction, often containing arbitrary or extra nonce data used by miners. |
| **transaction_count** | Number of transactions in the block. |
| **witness_count**     | Number of SegWit (witness) transactions in the block. |
| **input_count**       | Total number of input transactions in the block. |
| **output_count**      | Total number of output transactions in the block. |
| **input_total**       | Total amount of coins in input transactions. |
| **input_total_usd**   | Total value of coins in input transactions, converted to USD. |
| **output_total**      | Total amount of coins in output transactions. |
| **output_total_usd**  | Total value of coins in output transactions, converted to USD. |
| **fee_total**         | Total transaction fees from the block. |
| **fee_total_usd**     | Total transaction fees from the block, converted to USD. |
| **fee_per_kb**        | Average transaction fee per kilobyte of data in the block. |
| **fee_per_kb_usd**    | Average transaction fee per kilobyte, converted to USD. |
| **fee_per_kwu**       | Average transaction fee per kiloweight unit (relevant for SegWit). |
| **fee_per_kwu_usd**   | Average fee per kiloweight unit, converted to USD. |
| **cdd_total**         | Coin Days Destroyed, a measure of economic activity. Indicates the total days since coins in input transactions were last spent. |
| **generation**        | The amount of new coins generated in the block (block reward). |
| **generation_usd**    | Value of new coins generated in the block, converted to USD. |
| **reward**            | Total reward for mining the block (block reward + transaction fees). |
| **reward_usd**        | Total reward for mining the block, converted to USD. |
| **guessed_miner**     | An estimation of which miner or mining pool mined the block. |

## included columns
the following describes which columns will be present in the dataset

| Column Name         | Included/Redundant | Reason |
|---------------------|--------------------|--------|
| **Block ID**        | Included           | Unique identifier for each block; vital for tracking. |
| **hash**            | Included           | Cryptographic integrity; unique block identification. |
| **time**            | Included           | Helps in understanding block generation rate and patterns. |
| **median_time**     | Included           | Prevents timestamp manipulation; important for blockchain integrity. |
| **size**            | Included           | Provides insights on block capacity and network usage. |
| **stripped_size**   | Redundant          | Mostly relevant for specific SegWit analyses; can be derived from other data if needed. |
| **weight**          | Redundant          | Relevant for SegWit, but often used in combination with size metrics. |
| **version**         | Included           | Indicates block validation rules; can show evolution of the protocol. |
| **version_hex**     | Redundant          | Redundant if "version" is included; just a different representation. |
| **version_bits**    | Redundant          | Redundant if "version" is included; just a different representation. |
| **merkle_root**     | Included           | Essential for verifying transaction integrity within the block. |
| **nonce**           | Included           | Vital for understanding mining and proof-of-work. |
| **bits**            | Included           | Compact representation of the target difficulty. |
| **difficulty**      | Included           | Indicates how hard it was to mine the block. |
| **chainwork**       | Included           | Gives insight into cumulative work done until this block. |
| **coinbase_data_hex** | Included        | Often arbitrary data; not always crucial for block analysis. |
| **transaction_count** | Included         | Gives insights into block's transactional activity. |
| **witness_count**     | Redundant        | Relevant for SegWit but can be derived from transaction details if needed. |
| **input_count**       | Included         | Provides understanding of transaction input activity. |
| **output_count**      | Included         | Provides understanding of transaction output activity. |
| **input_total**       | Included         | Essential for understanding block's economic activity. |
| **input_total_usd**   | Redundant        | Conversion to USD might change over time; raw coin values are more stable for analysis. |
| **output_total**      | Included         | Essential for understanding block's economic output. |
| **output_total_usd**  | Redundant        | Same reason as "input_total_usd". |
| **fee_total**         | Included         | Indicates the total transaction fees; provides economic context. |
| **fee_total_usd**     | Redundant        | Conversion to USD might change; raw coin values preferred. |
| **fee_per_kb**        | Redundant        | Can be derived from "fee_total" and "size" if needed. |
| **fee_per_kb_usd**    | Redundant        | USD conversion not always relevant for block-level analysis. |
| **fee_per_kwu**       | Redundant        | Relevant for SegWit but can be derived if needed. |
| **fee_per_kwu_usd**   | Redundant        | Same reason as "fee_per_kb_usd". |
| **cdd_total**         | Included         | Provides an economic activity metric. |
| **generation**        | Included         | Indicates new coins generated; provides insight into block rewards. |
| **generation_usd**    | Redundant        | USD conversion can be derived externally if required. |
| **reward**            | Included         | Total miner reward; important for economic understanding. |
| **reward_usd**        | Redundant        | Same reason as "generation_usd". |
| **guessed_miner**     | Included         | Useful for understanding miner distribution and centralization. |
