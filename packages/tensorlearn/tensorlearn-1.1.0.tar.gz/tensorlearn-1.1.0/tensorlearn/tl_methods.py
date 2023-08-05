
    

from tensorlearn.decomposition import tensor_train
from tensorlearn.operations import tensor_operations as top
from tensorlearn.operations import matrix_operations as mop

def auto_rank_tt(tensor,epsilon):
    return tensor_train.auto_rank_tt(tensor,epsilon)
    
def unfold(tensor, n):
    return top.unfold(tensor, n)

def tt_to_tensor(factors):
    return top.tt_to_tensor(factors)
    
def tensor_resize(tensor, new_shape):
    return top.tensor_resize(tensor,new_shape)
    
def tensor_frobenius_norm(tensor):
    return top.tensor_frobenius_norm(tensor)
    
def error_truncated_svd(x, error):
    return mop.error_truncated_svd(x,error)

def tt_compression_ratio(factors):
    return top.tt_compression_ratio(factors)



    







