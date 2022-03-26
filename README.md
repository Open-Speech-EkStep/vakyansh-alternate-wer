# vakyansh-alternate-wer

### To create your modifed test set

```python
cd scripts/ 
python make_test_set_modified.py i <abs path to reference file> -o <abs path to modified reference file> -d <abs path to dictionary>
```
### To infer from modified test set reference file

```python
cd scripts/
wer_wav2vec_alternate_spelling.py -o <hypothesis file> -p <modified refernce file> -a True
```
