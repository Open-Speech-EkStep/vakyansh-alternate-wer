### Inference guide for opensourced results

## To infer on Vakyansh Hindi benchmarking data on  Viterbi output, run:

```python
cd scripts/
#results with alternate wer
python wer_wav2vec_alternate_spelling.py -o <abs path>vakyansh-alternate-wer/results/vakyansh_benchmarking_data/viterbi/hypo.word-checkpoint_best.pt-test.txt -p <abs path>vakyansh-alternate-wer/results/vakyansh_benchmarking_data/viterbi/alt_wer_format_ref.word-checkpoint_best.pt-test.txt -a True

#results without alternate wer
python wer_wav2vec_alternate_spelling.py -o <abs path>vakyansh-alternate-wer/results/vakyansh_benchmarking_data/viterbi/hypo.word-checkpoint_best.pt-test.txt -p <abs path>vakyansh-alternate-wer/results/vakyansh_benchmarking_data/viterbi/ref.word-checkpoint_best.pt-test.txt -a False

```


## To infer on Vakyansh Hindi benchmarking data on LM output, run:

```python
cd scripts/
#results with alternate wer
python wer_wav2vec_alternate_spelling.py -o <abs path>vakyansh-alternate-wer/results/vakyansh_benchmarking_data/lm/hypo.word-checkpoint_best.pt-test.txt -p <abs path>vakyansh-alternate-wer/results/vakyansh_benchmarking_data/lm/alt_wer_format_ref.word-checkpoint_best.pt-test.txt -a True

#results without alternate wer
python wer_wav2vec_alternate_spelling.py -o <abs path>vakyansh-alternate-wer/results/vakyansh_benchmarking_data/lm/hypo.word-checkpoint_best.pt-test.txt -p <abs path>vakyansh-alternate-wer/results/vakyansh_benchmarking_data/lm/ref.word-checkpoint_best.pt-test.txt -a False

```
