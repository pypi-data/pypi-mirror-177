# -*- coding: utf-8 -*-
"""
shorthand one-line API
"""
import indago


def minimize(evaluation_function, 
             dimensions, 
             lb, 
             ub, 
             optimizer_name, 
             optimize_seed=None,
             **kwargs):

    assert optimizer_name in indago.optimizers_name_list, \
        f'Unknown optimizer name "{optimizer_name}". Use one of the following names: {", ".join(indago.optimizers_name_list)}.'

    opt = indago.optimizers_dict[optimizer_name]()
    opt.evaluation_function = evaluation_function
    opt.dimensions = dimensions
    opt.lb = lb
    opt.ub = ub
    for kw, val in kwargs.items():
        setattr(opt, kw, val)
        # print(f'{kw=}: {val=}')
    result = opt.optimize(seed=optimize_seed)
        
    return result.X, result.f
