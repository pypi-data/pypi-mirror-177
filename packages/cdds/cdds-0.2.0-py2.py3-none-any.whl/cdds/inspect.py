"""Functions for inspecting objects, classes, and files"""

def get_methods(obj,private=False):
    """
    Retrieves a list of all non-private methods (default) from inside of obj.
    - If private==False: only returns methods whose names do NOT start with a '_'
    
    Args:
        obj (object): Object to retrieve methods from.
        private (bool): Whether to retrieve private methods or public.

    Returns:
        list: the names of all of the retrieved methods.
    """
    method_list = [func for func in dir(obj) if callable(getattr(obj, func))]
    if private:
        filt_methods = list(filter(lambda x: '_' in x[0] ,method_list))
    else:
        filt_methods = list(filter(lambda x: '_' not in x[0] ,method_list))
    return  filt_methods


def get_attributes(obj,private=False):
    """
    Retrieves a list of all non-private attributes (default) from inside of obj.
    - If private==False: only returns methods whose names do NOT start with a '_'
    
    Args:
        obj (object): Object to retrieve attributes from.
        private (bool): Whether to retrieve private attributes or public.
    
    Returns:
        list: the names of all of the retrieved attributes.
    """
    method_list = [func for func in dir(obj) if not callable(getattr(obj, func))]
    if private:
        filt_methods = list(filter(lambda x: '_' in x[0] ,method_list))
    else:
        filt_methods = list(filter(lambda x: '_' not in x[0] ,method_list))
    return  filt_methods


def get_methods_attributes_df(obj,include_private=False):
    """
    Retrieves all attributes and methods (with docstrings)
    and returns them in a DataFrame. By default only retrieves
    non-private methods, unless include_privates==True
    Args:
        obj (object): object to retrieve methods/attributes from
        include_privates (bool): Whether to include private methods/attributes
    
    Returns:
        Frame: DataFrame with results.
    """
    import pandas as pd
    methods = get_methods(obj,private=False)
    method_types = ['Method' for item in methods]

    attrs = get_attributes(obj,private=False)
    att_types =['Attribute' for item in attrs]
    
    if include_private:
        private_methods = get_methods(obj,private=True)
        methods.extend(private_methods)
        method_types.extend(['Private Method' for item in private_methods])
        
        private_attrs = get_attributes(obj,private=True)
        attrs.extend(private_attrs)
        att_types.extend(['Private Attribute' for item in private_attrs])
    
    
    docs=[]
    for m in methods:
        att = getattr(obj,m)
        docs.append(att.__doc__)

    all_res = [*methods,*attrs]
    res_type = [*method_types,*att_types]#['Method' for item in methods]+['Attribute' for item in attrs]
    docstrings= docs + ['na' for i in attrs]

    df_obj = pd.DataFrame({'Object':all_res,'Type':res_type,'Doc':docstrings})
    return df_obj



def ihelp(function_or_mod, show_help=False, show_code=True,return_code=False,markdown=True,file_location=False):
    """Call on any module or functon to display the object's
    help command printout AND/OR soruce code displayed as Markdown
    using Python-syntax"""
    import inspect
    
    try:
        from IPython.display import display, Markdown
    except:
        print('[!] IPython was not found.')
        
    page_header = '---'*28
    # footer = '---'*28+'\n'
    if show_help:
        print(page_header)
        banner = ''.join(["---"*2,' HELP ',"---"*24,'\n'])
        print(banner)
        help(function_or_mod)
        # print(footer)
        
    import sys
    if "google.colab" in sys.modules:
        markdown=False

    if show_code:
        print(page_header)

        banner = ''.join(["---"*2,' SOURCE -',"---"*23])
        print(banner)
        try:
            import inspect
            source_DF = inspect.getsource(function_or_mod)

            if markdown == True:
                
                output = "```python" +'\n'+source_DF+'\n'+"```"
                display(Markdown(output))
            else:
                print(source_DF)

        except TypeError:
            pass
            # display(Markdown)


    if file_location:
        file_loc = inspect.getfile(function_or_mod)
        banner = ''.join(["---"*2,' FILE LOCATION ',"---"*21])
        print(page_header)
        print(banner)
        print(file_loc)

    # print(footer)

    if return_code:
        return source_DF



def ihelp_menu(function_list,box_style='warning', to_embed=False):#, to_file=False):#, json_file='ihelp_output.txt' ):
    """
    Creates a widget menu of the source code and and help documentation of the functions in function_list.
    
    Args:
        function_list (list): list of function object or string names of loaded function. 
        to_embed (bool, optional): Returns interface (layout,output) if True. Defaults to False.
        to_file (bool, optional): Save . Defaults to False.
        json_file (str, optional): [description]. Defaults to 'ihelp_output.txt'.
        
    Returns:
        full_layout (ipywidgets GridBox): Layout of interface.
        output ()
    """
    
    # Accepts a list of string names for loaded modules/functions to save the `help` output and 
    # inspect.getsource() outputs to dictionary for later reference and display
    ## One way using sys to write txt file
    import pandas as pd
    import sys
    import inspect
    from io import StringIO
    from IPython.display import display,Markdown
    notebook_output = sys.stdout
    result = StringIO()
    sys.stdout=result
    
    ## Turn single input into a list
    if isinstance(function_list,list)==False:
        function_list = [function_list]
    
    ## Make a dictionary of{function_name : function_object}
    functions_dict = dict()
    for fun in function_list:
        
        ## if input is a string, save string as key, and eval(function) as value
        if isinstance(fun, str):
            functions_dict[fun] = eval(fun)

        ## if input is a function, get the name of function using inspect and make key, function as value
        elif inspect.isfunction(fun):

            members= inspect.getmembers(fun)
            member_df = pd.DataFrame(members,columns=['param','values']).set_index('param')

            fun_name = member_df.loc['__name__'].values[0]
            functions_dict[fun_name] = fun
            
            
    ## Create an output dict to store results for functions
    output_dict = {}

    for fun_name, real_func in functions_dict.items():
        
        output_dict[fun_name] = {}
                
        ## First save help
        help(real_func)
        output_dict[fun_name]['help'] = result.getvalue()
        
        ## Clear contents of io stream
        result.truncate(0)
                
        try:
            ## Next save source
            source_DF = inspect.getsource(real_func)
            # # if markdown == True:
                
            #     output = "```python" +'\n'+source_DF+'\n'+"```"
            #     display(Markdown(output))
            # else:
            #     output=source_DF
            print(source_DF)
            # output_dict[fun_name]['source'] = source_DF

            # print(inspect.getsource(real_func)) #eval(fun)))###f"{eval(fun)}"))
        except:
            # print("Source code for object was not found")
            print("Source code for object was not found")


        # finally:
        output_dict[fun_name]['source'] = result.getvalue()
        ## clear contents of io stream
        result.truncate(0)
    
        
        ## Get file location
        try:
            file_loc = inspect.getfile(real_func)
            print(file_loc)
        except:
            print("File location not found")
            
        output_dict[fun_name]['file_location'] =result.getvalue()
        
        
        ## clear contents of io stream
        result.truncate(0)        
        
    ## Reset display back to notebook
    sys.stdout = notebook_output    

    # if to_file==True:    
    #     with open(json_file,'w') as f:
    #         import json
    #         json.dump(output_dict,f)

    ## CREATE INTERACTIVE MENU
    from ipywidgets import interact, interactive, interactive_output
    import ipywidgets as widgets
    from IPython.display import display
    # from functions_combined_BEST import ihelp
    # import functions_combined_BEST as ji

    ## Check boxes
    check_help = widgets.Checkbox(description="Show 'help(func)'",value=True)
    check_source = widgets.Checkbox(description="Show source code",value=True)
    check_fileloc=widgets.Checkbox(description="Show source filepath",value=False)
    check_boxes = widgets.HBox(children=[check_help,check_source,check_fileloc])

    ## dropdown menu (dropdown, label, button)
    dropdown = widgets.Dropdown(options=list(output_dict.keys()))
    label = widgets.Label('Function Menu')
    button = widgets.ToggleButton(description='Show/hide',value=False)
    
    ## Putting it all together
    title = widgets.Label('iHelp Menu: View Help and/or Source Code')
    menu = widgets.HBox(children=[label,dropdown,button])
    titled_menu = widgets.VBox(children=[title,menu])
    full_layout = widgets.GridBox(children=[titled_menu,check_boxes],box_style=box_style)
    

    ## Define output manager
    # show_output = widgets.Output()

    def dropdown_event(change): 
        new_key = change.new
        output_display = output_dict[new_key]
    dropdown.observe(dropdown_event,names='values')

    
    def show_ihelp(display_help=button.value,function=dropdown.value,
                   show_help=check_help.value,show_code=check_source.value, 
                   show_file=check_fileloc.value,ouput_dict=output_dict):

        from IPython.display import Markdown
        # import functions_combined_BEST as ji
        from IPython.display import display        
        page_header = '---'*28
        # import json
        # with open(json_file,'r') as f:
        #     output_dict = json.load(f)
        func_dict = output_dict[function]
        source_code=None

        if display_help:
            if show_help:
#                 display(print(func_dict['help']))
                print(page_header)
                banner = ''.join(["---"*2,' HELP ',"---"*24,'\n'])
                print(banner)
                print(func_dict['help'])

            if show_code:
                print(page_header)

                banner = ''.join(["---"*2,' SOURCE -',"---"*23])
                print(banner)

                source_code = func_dict['source']#.encode('utf-8')
                if source_code.startswith('`'):
                    source_code = source_code.replace('`',"").encode('utf-8')

                if 'google.colab' in sys.modules:
                    print(source_code)
                else:
                    md_source = "```python\n"+source_code
                    md_source += "```"
                    display(Markdown(md_source))
            
            
            if show_file:
                print(page_header)
                banner = ''.join(["---"*2,' FILE LOCATION ',"---"*21])
                print(banner)
                
                file_loc = func_dict['file_location']
                print(file_loc)
                
            if show_help==False & show_code==False & show_file==False:
                display('Check at least one "Show" checkbox for output.')
                
        else:
            display('Press "Show/hide" for display')
            
    ## Fully integrated output
    output = widgets.interactive_output(show_ihelp,{'display_help':button,
                                                   'function':dropdown,
                                                   'show_help':check_help,
                                                   'show_code':check_source,
                                                   'show_file':check_fileloc})
    if to_embed:
        return full_layout, output
    else:
        display(full_layout, output)
              
        
def inspect_variables(local_vars = None,sort_col='size',exclude_funcs_mods=True, top_n=10,return_df=False,always_display=True,
show_how_to_delete=False,print_names=False):
    """
    Displays a dataframe of all variables and their size in memory,
    with the largest variables at the top. 
    
    Args:
        local_vars (locals(): Must call locals()  as first argument.
        sort_col (str, optional): column to sort by. Defaults to 'size'.
        top_n (int, optional): how many vars to show. Defaults to 10.
        return_df (bool, optional): If True, return df instead of just showing df.Defaults to False.
        always_display (bool, optional): Display df even if returned. Defaults to True.
        show_how_to_delete (bool, optional): Prints out code to copy-paste into cell to del vars. Defaults to False.
        print_names (bool, optional): [description]. Defaults to False.
    
    Raises:
        Exception: if locals() not passed as first arg
    
    
    Example Usage:
    # Must pass in local variables
    >> inspect_variables(locals())
    # To see command to delete list of vars"
    >> inspect_variables(locals(),show_how_to_delete=True)
    """
    
    

    import sys
    import inspect
    import pandas as pd
    from IPython.display import display
    if local_vars is None:
        raise Exception('Must pass "locals()" in function call. i.e. inspect_variables(locals())')


    glob_vars= [k for k in globals().keys()]
    loc_vars = [k for k in local_vars.keys()]

    var_list = glob_vars+loc_vars

    var_df = pd.DataFrame(columns=['variable','size','type'])

    exclude = ['In','Out']
    var_list = [x for x in var_list if (x.startswith('_') == False) and (x not in exclude)]

    i=0
    for var in var_list:#globals().items():#locals().items():

        if var in loc_vars:
            real_var = local_vars[var]
        elif var in glob_vars:
            real_var = globals()[var]
        else:
            print(f"{var} not found.")

        var_size = sys.getsizeof(real_var)

        var_type = []
        if inspect.isfunction(real_var):
            var_type = 'function'
            if exclude_funcs_mods:
                continue
        elif inspect.ismodule(real_var):
            var_type = 'module'
            if exclude_funcs_mods:
                continue
        elif inspect.isbuiltin(real_var):
            var_type = 'builtin'
        elif inspect.isclass(real_var):
            var_type = 'class'
        else:

            var_type = real_var.__class__.__name__


        var_row = pd.Series({'variable':var,'size':var_size,'type':var_type})
        var_df.loc[i] = var_row#pd.concat([var_df,var_row],axis=0)#.join(var_row,)
        i+=1

    # if exclude_funcs_mods:
    #     var_df = var_df.loc[var_df['type'] not in ['function', 'module'] ]

    var_df.sort_values(sort_col,ascending=False,inplace=True)
    var_df.reset_index(inplace=True,drop=True)
    var_df.set_index('variable',inplace=True)
    var_df = var_df[['type','size']]

    if top_n is not None:
        var_df = var_df.iloc[:top_n]



    if always_display:
        display(var_df.style.set_caption('Current Variables by Size in Memory'))

    if show_how_to_delete:
        print('---'*15)
        print('## CODE TO DELETE MANY VARS AT ONCE:')
        show_del_me_code(called_by_inspect_vars=True)


    if print_names ==False:
        print('#[i] set `print_names=True` for var names to copy/paste.')
        print('---'*15)
    else:
        print('---'*15)
        print('Variable Names:\n')
        print_me = [f"{str(x)}" for x in var_df.index]
        print(print_me)
    
        
    if show_del_me_code == False:
        print("[i] set `show_del_me_code=True prints copy/paste var deletion code.")
        

    if return_df:
        return var_df




def show_del_me_code(called_by_inspect_vars=False):
    """Prints code to copy and paste into a cell to delete vars using a list of their names.
    Companion function inspect_variables(locals(),print_names=True) will provide var names tocopy/paste """
    from pprint import pprint
    if called_by_inspect_vars==False:
        print("#[i]Call: `inspect_variables(locals(), print_names=True)` for list of var names")

    del_me = """
    del_me= []#list of variable names
    for me in del_me:
        try:
            exec(f'del {me}')
            print(f'del {me} succeeded')
        except:
            print(f'del {me} failed')
            continue
        """
    print(del_me)



def save_ihelp_to_file(function,save_help=False,save_code=True, 
                        as_md=False,as_txt=True,
                        folder='readme_resources/ihelp_outputs/',
                        filename=None,file_mode='w'):
    """Saves the string representation of the ihelp source code as markdown. 
    Filename should NOT have an extension. .txt or .md will be added based on
    as_md/as_txt.
    If filename is None, function name is used."""

    if as_md & as_txt:
        raise Exception('Only one of as_md / as_txt may be true.')

    import sys
    from io import StringIO
    ## save original output to restore
    orig_output = sys.stdout
    ## instantiate io stream to capture output
    io_out = StringIO()
    ## Redirect output to output stream
    sys.stdout = io_out
    
    if save_code:
        print('### SOURCE:')
        help_md = get_source_code_markdown(function)
        ## print output to io_stream
        print(help_md)
        
    if save_help:
        print('### HELP:')
        help(function)
        
    ## Get printed text from io stream
    text_to_save = io_out.getvalue()
    

    ## MAKE FULL FILENAME
    if filename is None:

        ## Find the name of the function
        import re
        func_names_exp = re.compile(r'def (\w*)\(')
        func_name = func_names_exp.findall(text_to_save)[0]    
        print(f'Found code for {func_name}')

        save_filename = folder+func_name#+'.txt'
    else:
        save_filename = folder+filename

    if as_md:
        ext = '.md'
    elif as_txt:
        ext='.txt'

    full_filename = save_filename + ext
    
    with open(full_filename,file_mode) as f:
        f.write(text_to_save)
        
    print(f'Output saved as {full_filename}')
    
    sys.stdout = orig_output



def get_source_code_markdown(function):
    """Retrieves the source code as a string and appends the markdown
    python syntax notation"""
    import inspect
    from IPython.display import display, Markdown
    source_DF = inspect.getsource(function)            
    output = "```python" +'\n'+source_DF+'\n'+"```"
    return output




def list2df(list, index_col=None, caption=None, return_df=True,df_kwds={}): #, sort_values='index'):  
    """ Quick turn an appened list with a header (row[0]) into a pretty dataframe.
        
        Args
            list (list of lists):
            index_col (string): name of column to set as index; None (Default) has integer index.
            set_caption (string):
            show_and_return (bool):
    
    EXAMPLE USE:
    >> list_results = [["Test","N","p-val"]] 
    
    # ... run test and append list of result values ...
    
    >> list_results.append([test_Name,length(data),p])
    
    ## Displays styled dataframe if caption:
    >> df = list2df(list_results, index_col="Test",
                     set_caption="Stat Test for Significance")
    """
    from IPython.display import display
    import pandas as pd
    df_list = pd.DataFrame(list[1:],columns=list[0],**df_kwds)
    
        
    if index_col is not None:
        df_list.reset_index(inplace=True)
        df_list.set_index(index_col, inplace=True)
        
    if caption is not None:
        dfs = df_list.style.set_caption(caption)
        display(dfs)
    return df_list


def arr2series(array,series_index=None, series_name='array'):
    """
    Converts an array into a named series. 
    
    Args:
        array (numpy array): Array to transform.
        series_index (list, optional): List of values to be used as index.
                                    Defaults to None, a numerical index.
        series_name (str, optional): Name for series. Defaults to 'array'.
    
    Returns:
        converted_array: Pandas Series with the name and index specified. 
    """
    import pandas as pd
    if len(series_index)==0:
        series_index=list(range(len(array)))

    if len(series_index)>len(array):
        new_index= series_index[-len(array):]
        series_index=new_index

    converted_array = pd.Series(array.ravel(), index=series_index, name=series_name)
    return converted_array




def column_report(df,index_col=None, sort_column='iloc', ascending=True,
                  interactive=False, return_df=False):
    """
    Displays a DataFrame summary of each column's: 
    - name, iloc, dtypes, null value count & %, # of 0's, min, max,med,mean, etc
    
    Args:
        df (DataFrame): df to report 
        index_col (column to set as index, str): Defaults to None.
        sort_column (str, optional): [description]. Defaults to 'iloc'.
        ascending (bool, optional): [description]. Defaults to True.
        as_df (bool, optional): [description]. Defaults to False.
        interactive (bool, optional): [description]. Defaults to False.
        return_df (bool, optional): [description]. Defaults to False.

    Returns:
        column_report (df): Non-styled version of displayed df report
    """
    from ipywidgets import interact
    import pandas as pd
    from IPython.display import display

    def count_col_zeros(df, columns=None):
        import pandas as pd
        import numpy as np
        # Make a list of keys for every column  (for series index)
        zeros = pd.Series(index=df.columns)
        # use all cols by default
        if columns is None:
            columns=df.columns

        # get sum of zero values for each column
        for col in columns:
            zeros[col] = np.sum( df[col].values == 0)
        return zeros


    ##
    df_report = pd.DataFrame({'.iloc[:,i]': range(len(df.columns)),
                            'column name':df.columns,
                            'dtypes':df.dtypes.astype('str'),
                            '.isna()': df.isna().sum().round(),
                            '% na':df.isna().sum().divide(df.shape[0]).mul(100).round(2),
                            '# zeros': count_col_zeros(df),
                            '# unique':df.nunique(),
                            'min':df.min(),
                            'max':df.max(),
                            'med':df.describe().loc['50%'],
                            'mean':df.mean().round(2)})#
    ## Sort by index_col
    if index_col is not None:
        hide_index=False
        if 'iloc' in index_col:
            index_col = '.iloc[:,i]'

        df_report.set_index(index_col ,inplace=True)
    else:
        hide_index=True


    ##  Sort column
    if sort_column is None:
        sort_column = '.iloc[:,i]'


    if 'iloc' in sort_column:
        sort_column = '.iloc[:,i]'

    df_report.sort_values(by =sort_column,ascending=ascending, axis=0, inplace=True)

    dfs = df_report.style.set_caption('Column Report')
    
    if hide_index:
        display(dfs.hide_index())
    else:
        display(dfs)   

    if interactive:
        @interact(column= df_report.columns,direction={'ascending':True,'descending':False})
        def sort_df(column, direction):
            return df_report.sort_values(by=column,axis=0,ascending=direction)
    if return_df:
        return df_report
        
        
        


def check_package_versions(packages = ['matplotlib','seaborn','pandas','numpy','sklearn','fsds'],
                           fpath=False, show_only=True):
    """Imports packages and saves the name and version number to a dataframe"""
    import pandas as pd
    import inspect
    from cdds.imports import global_imports
    version_list = [['Package','Version']]
    
    ## Remove submodules from version check (wont have version #)
    for package in packages:
        if '.' not in package:
            try:
                ## use global imports and retrieve version #
                vers = global_imports(package,None,check_vers=True)
            except:
                vers = '!'
            version_list.append([package,vers])

    # Convert to df
    pkg_vers_df = pd.DataFrame(version_list[1:],columns=version_list[0])
    
    ## If get_fpath
    if fpath==True:
        pkg_vers_df['File'] = pkg_vers_df['Package'].map(lambda x: inspect.getsourcefile(globals()[x]))
        # for package in packages:
    
    if show_only==True: 
        if fpath==True:   
            dfs = pkg_vers_df.style.set_properties(subset='File',
                                                **{'width':"600px","text-align":'center'})
        else:
            dfs = pkg_vers_df.style
        display(dfs.set_caption('Package Versions'))
    
        
    else:
        return pkg_vers_df
        

import os
def get_df_memory_usage(df,units='mb'):
	"""returns memory size of dataframe in requested units"""
	memory = df.memory_usage().sum()
	if units.lower()=='mb':
		denom = 1e6
	elif units.lower()=='gb':
		denom = 1e9
	elif units.lower()=='kb':
		denom = 1e3
	else:
		raise Exception('Units must be either "mb" or "gb"')
	val = memory/denom
	print(f"- Total Memory Usage = {val} {units.upper()}")
    
    
def get_filesize(fname, units='mb'):
	"""Get size of file at given path in MB or GB"""
	if units.lower()=='mb':
		denom = 1e6
	elif units.lower()=='gb':
		denom = 1e9
	elif units.lower()=='kb':
		denom = 1e3
	else:
		raise Exception('Units must be "kb","mb", or "gb"')
		
	import os
	size = os.path.getsize(fname)

	val = size/denom
	# str_val = f"{val} {units.upper()}"
	print(f"- {fname} is {val} {units.upper()} on disk.")

	return val
	


def get_file_info(fname, units='mb'):
	"""Returns a dictionary with detailed file information including:
	- File name, extension, file size, date created, date modified, etc.
	Args:
		fname (str): filepath
		units (str, optional): Units for fileszize. (Options are "kb','mb','gb'). Defaults to 'mb'.

	Returns:
		dict: dictionary with info
	"""
	import time
	import os
	import pandas as pd
	
	## Get file created and modified time
	modified_time = time.ctime(os.path.getmtime(fname))
	created_time = time.ctime(os.path.getctime(fname))
	
	## Get file size 
	raw_size = os.path.getsize(fname)
	size = get_filesize(fname,units=units)
	str_size = f"{size} {units}"
	
	# Get path info
	rel_path = os.path.relpath(fname)
	abs_path =  os.path.abspath(fname)
	_, ext = os.path.splitext(fname)
	basename =os.path.basename(fname)
	dirname = os.path.dirname(fname)
	
	file_info ={"Filepath": fname,"Name":basename, 'Created':created_time, 'Modified':modified_time,  'Size':str_size,
	'Folder':dirname,"Ext":ext, "Size (bytes)":raw_size,
	'Relative Path':rel_path,'Absolute Path':abs_path}
	
	return file_info



import pandas as pd
import json
import tmdbsimple as tmdb



def read_and_fix_json(JSON_FILE):
    """Attempts to read in json file of records and fixes the final character
    to end with a ] if it errors.
    
    Args:
        JSON_FILE (str): filepath of JSON file
        
    Returns:
        DataFrame: the corrected data from the bad json file
    """
    try: 
        previous_df =  pd.read_json(JSON_FILE)
    
    ## If read_json throws an error
    except:
        
        ## manually open the json file
        with open(JSON_FILE,'r+') as f:
            ## Read in the file as a STRING
            bad_json = f.read()
            
            ## if the final character doesn't match first, select the right bracket
            first_char = bad_json[0]
            final_brackets = {'[':']', 
                           "{":"}"}
            ## Select expected final brakcet
            final_char = final_brackets[first_char]
            
            ## if the last character in file doen't match the first char, add it
            if bad_json[-1] != final_char:
                good_json = bad_json[:-1]
                good_json+=final_char
            else:
                raise Exception('ERROR is not due to mismatched final bracket.')
            
            ## Rewind to start of file and write new good_json to disk
            f.seek(0)
            f.write(good_json)
           
        ## Load the json file again now that its fixed
        previous_df =  pd.read_json(JSON_FILE)
        
    return previous_df
	
	
	
	

def write_json(new_data, filename): 
    """Adapted from: https://www.geeksforgeeks.org/append-to-json-file-using-python/"""    
    
    with open(filename,'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        ## Choose extend or append
        if (type(new_data) == list) & (type(file_data) == list):
            file_data.extend(new_data)
        else:
             file_data.append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file)

	
	