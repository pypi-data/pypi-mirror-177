from multiprocessing import Pool, Manager
import traceback


def _pool_run_single_func(func, q_param, q_result):
    while True:
        try:
            data = q_param.get(block=False, timeout=0)
            index = data['index']
            param = data['param']
            skip_exception = data['skip_exception']
        except:
            break
        if skip_exception:
            try:
                ret = func(**param)
                q_result.put(
                    {
                        'index': index,
                        'data': ret
                    }
                )
            except:
                print(traceback.format_exc())
        else:
            ret = func(**param)
            q_result.put(
                {
                    'index': index,
                    'data': ret
                }
            )


def _pool_run_multiply_func(q_param, q_result):
    while True:
        try:
            data = q_param.get(block=False, timeout=0)
            index = data['index']
            param = data['param']
            func = param['func']
            del param['func']
            skip_exception = data['skip_exception']
        except:
            break
        if skip_exception:
            try:
                ret = func(**param)
                q_result.put(
                    {
                        'index': index,
                        'data': ret
                    }
                )
            except:
                print(traceback.format_exc())
        else:
            ret = func(**param)
            q_result.put(
                {
                    'index': index,
                    'data': ret
                }
            )

# 多进程多参数执行同一个函数
def pool_single_func(func, params, p_num=4, skip_exception=False):
    result_map = {}
    if p_num <= 1:
        for index, param in enumerate(params):
            data = func(**param)
            result_map[index] = data
    else:
        q_param = Manager().Queue()
        q_result = Manager().Queue()
        for index, param in enumerate(params):
            q_param.put(
                {'index': index, 'param': param, 'skip_exception': skip_exception}
            )

        pool = Pool(p_num)
        for i in range(p_num):
            pool.apply_async(
                func=_pool_run_single_func,
                kwds={
                    'func': func,
                    'q_param': q_param,
                    'q_result': q_result,
                }
            )
        pool.close()
        pool.join()

        for i in range(q_result.qsize()):
            result = q_result.get(block=False, timeout=0)
            index = result['index']
            data = result['data']
            result_map[index] = data
    return result_map


# 多进程多参数执行多个函数
def pool_multiply_func(params, p_num=4, skip_exception=False):
    result_map = {}
    if p_num <= 1:
        for index, param in enumerate(params):
            func = param['func']
            del param['func']
            data = func(**param)
            result_map[index] = data
    else:
        q_param = Manager().Queue()
        q_result = Manager().Queue()
        for index, param in enumerate(params):
            q_param.put(
                {'index': index, 'param': param, 'skip_exception': skip_exception}
            )
        pool = Pool(p_num)
        for i in range(p_num):
            pool.apply_async(
                func=_pool_run_multiply_func,
                kwds={
                    'q_param': q_param,
                    'q_result': q_result,
                }
            )
        pool.close()
        pool.join()

        for i in range(q_result.qsize()):
            result = q_result.get(block=False, timeout=0)
            index = result['index']
            data = result['data']
            result_map[index] = data
    return result_map
