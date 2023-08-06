import os
import sys
import yaml
import uuid
import time
import shutil
import datetime
import importlib
from .settings import config as _config
from functools import partial
from .common import get_uuid_by_given_name, get_folder_md5, add_obj_common, download_obj_from_server


def get_function_by_md5(md5):
    if md5 is not None:
        function_folder = os.path.join(_config['axiom_cache'], md5, 'obj')
        if not os.path.isdir(function_folder):
            download_obj_from_server(md5)
        sys.path.append(function_folder)
        print('function_folder', function_folder)
        run_file = 'main'
        x = importlib.import_module(run_file)
        print(x)
        return x.main
    sys.exit(0)

def get_function_by_given_name(given_name):
    md5 = get_uuid_by_given_name(given_name)
    return get_function_by_md5(md5)

def the_func(config={}, in_folders=[], given_names=[], out_folders=None, func_name=''):
    md5 = get_uuid_by_given_name(func_name)
    f = get_function_by_md5(md5)
    if out_folders is None:
        out_folders = []
        n = len(given_names)
        obj_folders = []
        for i in range(n):
            random_id = str(uuid.uuid4())
            out_folder = os.path.join(_config['axiom_cache'], random_id)
            obj_folder = os.path.join(out_folder, 'obj')
            obj_folders.append(obj_folder)
            print('making dir', obj_folder)
            os.makedirs(obj_folder)
            out_folders.append(out_folder)
    function_info = yaml.safe_load(open(os.path.join(_config['axiom_path'], 'info', md5+'.yaml')))
    if function_info['axiom_name'] == '__AXIOM__':
        function_info['axiom_name'] = md5
    print('function_info', function_info)
    t_begin = time.time()
    time_begin = str(datetime.datetime.now())
    f(config, in_folders, given_names, obj_folders)
    time_end = str(datetime.datetime.now())
    t_end = time.time()
    in_axiom_names = []
    for i in range(len(in_folders)):
        in_folder = in_folders[i]
        d = yaml.safe_load(open(os.path.join(os.path.split(in_folder)[0], 'info.yaml')).read())
        if d['axiom_name'] == '__AXIOM__':
            in_axiom_names.append(os.path.split(os.path.split(in_folder)[0])[-1])
        else:
            in_axiom_names.append(d['axiom_name'])


    print('in_axiom_names', in_axiom_names)
    info = {}
    uname = str(os.uname()).replace("'", '"').replace('\n', '')
    n_out = len(out_folders)
    for i in range(n_out):
        out_folder = out_folders[i]
        given_name = given_names[i]
        the_type = function_info['output'][i]
        description = 'data from function '+func_name
        info['type'] = the_type
        info['given_name'] = given_name
        info['axiom_name'] = {'function': function_info['axiom_name'], 'in_data': in_axiom_names, 'out': '%d/%d' % (i, n_out)}
        info['description'] = description
        info['run_begin_time'] = time_begin
        info['run_end_time'] = time_end
        info['running_time'] = t_end - t_begin
        info['uname'] = uname
        info_file = os.path.join(out_folder,'info.yaml')
        yaml.safe_dump(info, open(info_file, 'w'))
    for out_folder in out_folders:
        md5 = get_folder_md5(os.path.join(out_folder, 'obj')) # md5 is the one with obj folder
        print('out_folder',out_folder)
        md5_folder = os.path.join(os.path.split(out_folder)[0], md5)
        print('md5_folder', md5_folder)
        shutil.move(out_folder, md5_folder)
        add_obj_common(os.path.join(md5_folder, 'obj'))
    return out_folders




def main(func_name):
    print('axiom import', func_name)
    return partial(the_func, func_name=func_name)
