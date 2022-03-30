# vakyansh-alternate-wer

### To create your modifed test set

```python
cd scripts/ 
python make_test_set_modified.py i <abs path to reference.txt file> -o <abs path to modified_reference.txt file> -d <abs path to dictionary>
```
### To infer from modified test set reference file

```python
cd scripts/
python wer_wav2vec_alternate_spelling.py -o <hypothesis.txt> -p <modified_reference.txt file> -a True
```

## Analyzing Common Error words from the base reference file vs hypothesis file
To get the substituted word pairs, install the [SCTK](https://github.com/usnistgov/SCTK) tool.

```
git clone https://github.com/usnistgov/SCTK.git
make config
make all
make check
make install
make doc
```

Then run the file:
```bash
cd scripts/
bash get_results.sh <abs path to hypothesis.txt> <abs path to reference.txt> <abs path to output_folder>
```

Inside the output folder, reference.sgml or reference.dtl file will be created where you can manually see the most commonly substituted pairs, which can be added to the dictionary if the mappings are valid.

(Optional)To calculate error statistics, change the folder_name to <abs path to output_folder> in the error_word_statistics.py file and then run:
```
python error_word_statistics.py
```
  
### Open sourcing Vakyansh-benchmarking data
The link to the original 21 hours of data can be found at : [Vakyansh Benchmark Dataset without numbers](https://github.com/Open-Speech-EkStep/ULCA-asr-dataset-corpus#hindi-benchmark-datasets-total-duration-is-41-hours)

 To find the hypothesis, reference and modified_alt_wer_refernce_files as inferred from ASR model [him_4200.pt](https://github.com/Open-Speech-EkStep/vakyansh-alternate-wer/tree/main/results/vakyansh_benchmarking_data/lm) on [CLSRIL-23](https://github.com/Open-Speech-EkStep/vakyansh-alternate-wer/tree/main/results/vakyansh_benchmarking_data/lm):
 <br>
Viterbi : [link](https://github.com/Open-Speech-EkStep/vakyansh-alternate-wer/tree/main/results/vakyansh_benchmarking_data/viterbi)
<br>
LM output : [link](https://github.com/Open-Speech-EkStep/vakyansh-alternate-wer/tree/main/results/vakyansh_benchmarking_data/lm)
