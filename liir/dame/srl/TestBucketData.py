from liir.dame.srl.DataProcessor import DataProcessor
from liir.dame.core.nn.Data import BucketedDataIteratorSEQ
from liir.dame.core.io.CoNLL2005Reader import CoNLL2005Reader
import sys
if __name__ == "__main__":
    train_data_path = sys.argv[1]
    pp = DataProcessor(model_dir="test-bucket-data")
    pp.generate_vob(train_data_path)
    train_data_sens = CoNLL2005Reader(train_data_path).read_all()
    train_data = pp.get_data_train(train_data_path , data=train_data_sens)
    print("---------------Train data-------------")
    print(train_data)
    print("---------------Processed with Bucket-data-------------")
    train_input = BucketedDataIteratorSEQ(dt=train_data, num_buckets=2)
    print(train_input)
    print("---------------Processed with Bucket-data and next batch-------------")
    (inputs_vals, predicate_vals, srl_target_vals, ner_target_vals), seq_len_vals = train_input.next_batch(2)
    print(('input vals', inputs_vals))
    print(('predicate vals', predicate_vals))
    print(('srl target vals', srl_target_vals))
    print(('ner target vals', ner_target_vals))
    print(('seq len vals', seq_len_vals))
    pass