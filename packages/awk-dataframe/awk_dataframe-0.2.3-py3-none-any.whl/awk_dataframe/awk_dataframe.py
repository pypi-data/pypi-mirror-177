import re
import subprocess
import numpy as np
import pandas as pd
from copy import deepcopy
import time
import sys
import os
import numpy_dataframe as npd
import random
import string
import shutil



def awk_command_to_file(command):
    if not os.path.exists(os.path.expanduser('~') + "/.tmp/"):
        os.mkdir(os.path.expanduser('~') + "/.tmp/")
    if not os.path.exists(os.path.expanduser('~') + "/.tmp/awk_dataframe/"):
        os.mkdir(os.path.expanduser('~') + "/.tmp/awk_dataframe/")
        print("Creating folder ",os.path.expanduser('~') + "/.tmp/awk_dataframe/")

    path_sh = os.path.expanduser('~') + "/.tmp/awk_dataframe/execution_" + command.type + "_" + command.id + ".awk"
    command.path_execution_file = path_sh
    debug("composing command:",command.type)
    f = open(path_sh,'w')
    complete_command = compose_generic_command(command.options,commands_transform_column=command.commands["commands_transform_column"],commands_transform_digit=command.commands["commands_transform_digit"],command_transform_string=command.commands["command_transform_string"],command_transform_line=command.commands["command_transform_line"],command_condition=command.commands["command_condition"])
    f.write(complete_command)
    f.close()

def generic_functions_awk():
    # note("Thanks to Ed Morton: https://stackoverflow.com/questions/45420535/whats-the-most-robust-way-to-efficiently-parse-csv-using-awk/45420607#45420607")
    text = """
    function buildRec(      fpat,fldNr,fldStr,done) {
    #Thanks to Ed Morton: https://stackoverflow.com/questions/45420535/whats-the-most-robust-way-to-efficiently-parse-csv-using-awk/45420607#45420607

        if (level_simplicity_csv != 0){
            done = 1
            return done
        }else{
            CurrRec = CurrRec $0
            if ( gsub(/"/,"&",CurrRec) % 2 ) {
            # if (number_fields == 0 || NF != number_fields){
                # The string built so far in CurrRec has an odd number
                # of "s and so is not yet a complete record.
                CurrRec = CurrRec RS
                done = 0
            }
            else {
                # If CurrRec ended with a null field we would exit the
                # loop below before handling it so ensure that cannot happen.
                # We use a regexp comparison using a bracket expression here
                # and in fpat so it will work even if FS is a regexp metachar
                # or a multi-char string like "\\\input_quote for -separated fields.
                CurrRec = CurrRec ( CurrRec ~ ("[" FS "]$") ? input_quote input_quote : "" )
                $0 = ""
                fpat = "([^" FS "]*)|(" input_quote "([^" input_quote "]|" input_quote input_quote ")+" input_quote ")"
                while ( (CurrRec != "") && match(CurrRec,fpat) ) {
                    fldStr = substr(CurrRec,RSTART,RLENGTH)
                    # gsub(input_quote "NULL" input_quote,delimiter_internal_notation "NULL" delimiter_internal_notation, fldStr)
                    # gsub(input_quote "null" input_quote,delimiter_internal_notation "NULL" delimiter_internal_notation, fldStr)
                    # ### Convert <"foo"> to <foo> and <"foo""bar"> to <foo"bar>
                    # if (fields_based_code){
                    #     quotes_have_been_removed = 1
                    #     if (gsub("^" input_quote "|" input_quote "$","",fldStr)) {
                    #         gsub("(" input_quote ")", delimiter_internal_notation "q" delimiter_internal_notation, fldStr)
                    #     }
                    # }
                    $(++fldNr) = fldStr
                    CurrRec = substr(CurrRec,RSTART+RLENGTH+1)
                }
                CurrRec = ""
                done = 1
            }
            return done
        }
        return 1
    }

    function is_digit_field(field){
        if (field ~ /^[\\\\+-]?[0-9]+$|^[\\\\+-]*[0-9]*[\\\\.]?[0-9]+$|^[\\\\+-]*[0-9]*[\\\\.]?[0-9]+[eE]?[\\\\+-]?[0-9]+$|^nan$|^Nan$|^NaN$|^NAN$/){
            return 1
        }else{
            return 0
        }
    }

    function needs_quotes(field){
    #postgres_standard: delimiter character, the QUOTE character, the NULL string, a carriage return, or line feed character, t

        regex = "(" FS ")+|(\\\\n)+|(" input_quote ")+|\\r+"
        if (field ~ regex){
            return 1
        }else{
            return 0
        }
    }

    function transform_field(field,column){ 
        if (is_first_command && !is_last_command && original_level_simplicity_csv != 2){
            gsub(/\\n/,delimiter_internal_notation "n" delimiter_internal_notation,field)
            gsub(FS,delimiter_internal_notation "d" delimiter_internal_notation,field)
            # if (field == null_input_string){
            #     print "wtf"
            #     # gsub(null_input_string,null_output_string,field)
            # }
            gsub(input_quote, delimiter_internal_notation "q" delimiter_internal_notation, field)
            gsub("\\r", delimiter_internal_notation "r" delimiter_internal_notation, field)
        }
        if (is_last_command && !is_first_command  && original_level_simplicity_csv != 2){
            gsub(delimiter_internal_notation "n" delimiter_internal_notation,"\\n",field)
            gsub(delimiter_internal_notation "d" delimiter_internal_notation,FS,field)
            gsub(delimiter_internal_notation "q" delimiter_internal_notation,input_quote, field)
            gsub(delimiter_internal_notation "r" delimiter_internal_notation,"\\r", field)
        }       
        if (is_digit_field(field) || (level_simplicity_csv == 2 && (!is_last_command || original_level_simplicity_csv == 2))){
            if (!is_digit_field()){
                field = transform_string(field,column)
                if (input_quote != output_quote){
                    gsub(input_quote,output_quote,field)
                }
            }else{
                return transform_digit(field,column)
            }
            return field
        }else{
            field = transform_string(field,column)
            if (quotes_have_been_removed){
                if (full_string_quoting){
                    return output_quote field output_quote
                }else{
                    if (needs_quotes(field) && minimal_string_quoting || field == delimiter_internal_notation "NULL" delimiter_internal_notation){
                        if (field == delimiter_internal_notation "NULL" delimiter_internal_notation){
                            gsub(delimiter_internal_notation "NULL" delimiter_internal_notation,"NULL",field)
                        }
                        return output_quote field output_quote
                    }else{
                        return field
                    }
                }
            }else{
                return field
            }
        }

    }



    function print_field(field,column){

        
        field = transform_field(field,column)
        
        if (FNR == NR && find_unique){
            unique[field] = 1
        }else{
            if (print_fields){
                output_separator = OFS
                if (i == max_col() && !add_new_column){
                    output_separator = ORS
                }
                if (i == min_col()){
                    if (add_index){
                        if (!save){
                            printf("%s" output_separator,print_line_number() + index_based_on)
                        }else{
                            printf("%s" output_separator,print_line_number() + index_based_on) > path_output
                        }
                        
                    }
                }
                if (!save){
                    printf "%s" output_separator,field
                }else{
                    printf "%s" output_separator,field > path_output                    
                }
            
            }
        }
    }


    function print_line(line){
        line = transform_line(line)
        if (print_fields){
            if (add_index){
                if (!save){
                    printf("%s" OFS,print_line_number() + index_based_on)
                }else{
                    printf("%s" OFS,print_line_number() + index_based_on) > path_output
                }
                
            }
            if (input_quote != output_quote){
                gsub(input_quote,output_quote,line)
            }
        
            if (!save){
                if (sort){
                    sort_command = "sort -t'" OFS "' --parallel " num_cores " -nk" sort_column 
                    printf "%s" ORS,line | sort_command
                }else{
                    printf "%s" ORS,line
                }
            }else{
                printf "%s" ORS,line > path_output
            }
        }
    }

    function print_line_number(){
        if (output_header){
            return FNR-records_skipped - 2
        }else{
            return FNR-records_skipped - 1
        }
    }

    function line_number(){
        if (header){
            return FNR-records_skipped - 1
        }else{
            return FNR-records_skipped
        }

    }

    function print_header(){
        if (add_index){
            if (!save){
                printf("%s" OFS,output_quote "ad_internal_index" output_quote)
            }else{
                printf("%s" OFS,output_quote "ad_internal_index" output_quote) > path_output
            }
            
        }
        if (fields_based_code){
            for (i=min_col();i<=max_col();i++) {
                if ((number_files_input == 1 || input_file_rows) || (input_file_cols && v[i])){
                    if (is_first_command && !is_last_command && level_simplicity_csv != 2){
                        gsub(/\\n/,delimiter_internal_notation "n" delimiter_internal_notation,$i)
                        gsub(FS,delimiter_internal_notation "d" delimiter_internal_notation,$i)
                        # if ($i == null_input_string){
                        # gsub(null_input_string,null_output_string,$i)
                        # }
                        gsub(input_quote, delimiter_internal_notation "q" delimiter_internal_notation, $i)
                        gsub("\\r", delimiter_internal_notation "r" delimiter_internal_notation, $i)
                    }
                    if (is_last_command && !is_first_command  && level_simplicity_csv != 2){
                        gsub(delimiter_internal_notation "n" delimiter_internal_notation,"\\n",$i)
                        gsub(delimiter_internal_notation "d" delimiter_internal_notation,FS,$i)
                        gsub(delimiter_internal_notation "q" delimiter_internal_notation,input_quote, fldStr)
                        gsub(delimiter_internal_notation "r" delimiter_internal_notation,"\\r", $i)
                    }
                    output_separator = OFS
                    if (i == max_col() && !add_new_column){
                        output_separator = ORS
                    }
                    if (!save){
                        printf "%s" output_separator,transform_header($i,i)
                    }else{
                        printf "%s" output_separator,transform_header($i,i) > path_output
                    }
                }
                
            }
            add_column()
        }else{
            gsub(input_quote,output_quote,$0)
            if (!save){
                printf "%s" ORS,$0
            }else{
                printf "%s" ORS,$0 > path_output
            }
            add_column()
            
        }
        
    }

    function min_col(){
        if (1 > col_start){
            return 1
        }else{
            return col_start
        }
    }

    function max_col(){
        if (col_end == INF){
            return NF
        }else{
            if (NF < col_end){
                return NF
            }else{
                return col_end
            }
        }
    }

    function add_column(){
        if (add_new_column){
            if (line_number() == 0){
                printf "%s" ORS,name_new_column
            }else{
                printf "%s" ORS,""
            }
        }
    
    }

    function transform_header(field,column){
        return field
    }

    function process_fields(){
        if (level_simplicity_csv != 0){
            done = 1
            # return done

        }else{
                if (!continue_next_line){
                    current_field_index = 1
                    inside_string = 0
                    field = ""
                }else{
                    field = field ":n:"
                }
                

                for (i=1;i<=length($0);i++){
                    
                    if (inside_string){
                        if (is_first_command && !is_last_command && substr($0, i, 1) == ","){
                            field = field ":d:"
                        }else if (is_first_command && !is_last_command && substr($0, i, 1) == "\\r"){
                            field = field ":r:"
                        }else if (is_first_command && !is_last_command && substr($0, i, 1) == "\\"" && (i != length($0) && substr($0, i+1, 1) != ",")){
                            field = field ":q:"
                        }else{
                            field = field substr($0, i, 1)
                        }
                        if (substr($0, i, 1) == "\\"" && (i == length($0) || substr($0, i+1, 1) == ",")){
                            inside_string = 0                            
                        }
                    }else{
                        if (substr($0, i, 1) == "\\""){
                            inside_string = 1 
                            # print "inside string" field
                            field = field substr($0, i, 1)
                        }else{
                            if (substr($0, i, 1) == "," || i == length($0)){
                                if (i == length($0) && substr($0, i, 1) == ","){
                                    field = field substr($0, i, 1)    
                                    fields[current_field_index] = field
                                    field = ""     
                                    current_field_index += 1
                                    fields[current_field_index] = ""
                                }
                                else if (i == length($0)){
                                    field = field substr($0, i, 1)    
                                    fields[current_field_index] = field
                                    field = ""                  
                                                      
                                }else{
                                    fields[current_field_index] = field
                                    field = ""
                                    current_field_index += 1
                                    
                                }
                                
                                
                            }else{
                                field = field substr($0, i, 1)
                            }
                        }
                        
                    }
                }
                # print line_number()
                if (line_number() == 0){
                    field = ""
                    for (i=1;i<=current_field_index;i++){
                        $i = fields[i]
                    }
                    NF = current_field_index
                    $1 = $1                    
                    number_fields = current_field_index
                    continue_next_line = 0
                    done = 1
                    # return done
                }else{
                    if (inside_string){
                        continue_next_line = 1
                        records_skipped += 1
                        # next                
                        done = 0 
                        # return done
                    }
                    if (number_fields > current_field_index){
                        continue_next_line = 1
                        records_skipped += 1
                        # next
                        done = 0 
                        # return done
                    }else{
                        continue_next_line = 0
                        field = ""
                        for (i=1;i<=current_field_index;i++){
                            $i = fields[i]
                        }
                        NF = current_field_index
                        $1 = $1                    
                        done = 1
                        # return done
                    }
                }
        }
        # return done
    }


    #################################   
    #################################

    """
    return text



def function_transform_column(commands = ""):
    commands = """
    function transform_column(field,column){
    """ + commands +"""
    return field
    }

    """
    return commands

def function_transform_digit(commands = ""):
    commands = """
    function transform_digit(field,column){
    field = transform_column(field,column)
    """ + commands +"""
    return field
    }

    """
    return commands

def function_transform_string(commands = ""):
    commands = """
    function transform_string(field,column){
    field = transform_column(field,column)
    """ + commands +"""
    return field
    }
    """
    return commands

def function_transform_line(commands = ""):
    commands = """
    function transform_line(line){
    """ + commands +"""
    return line
    }
    """
    return commands


def function_condition(commands = ""):
    if commands != "":
        commands = """
        function condition(){
        statement = 1
        statement = (""" + commands +""")
        return statement
        }
        """
    else:
        commands = """
        function condition(){
        statement = 1        
        return statement
        }

    """
    return commands

def get_options_default():
    options = {}
    options["is_first_command"] = "1"
    options["is_last_command"] = "1"
    options["FS"] = ","
    options["OFS"] = ","
    options["input_quote"] = "\\\""
    options["output_quote"] = "\\\""
    options["level_simplicity_csv"] = "0"
    options["original_level_simplicity_csv"] = "0"
    options["minimal_string_quoting"] = "1"
    options["is_unix_input"] = "1"
    options["is_unix_output"] = "1"
    options["null_input_string"] = "NULL"
    options["null_output_string"] = ""
    options["header"] = "1"
    options["output_header"] = "1"
    options["add_index"] = "0"
    options["index_based_on"] = "0"
    options["line_based_code"] = "0"
    options["col_start"] = "1"
    options["col_end"] = "INF"
    options["row_start"] = "1"
    options["row_end"] = "INF"
    options["number_files_input"] = "1"
    options["input_file_rows"] = "1"
    options["find_unique"] = "0"
    options["print_fields"] = "1"
    options["save"] = "0"
    options["path_output"] = ""
    options["sort"] = "0"
    options["num_cores"] = "4"
    options["sort_column"] = "1"
    options["sort_in_parallel"] = "1"
    options["calculate_shape"] = "0"
    options["check_complexity"] = "0"
    options["add_new_column"] = "0"
    options["name_new_column"] = ""




    return options
    




def begin(options):
    
    command = """
    BEGIN {
        PREC=100
        OFMT="%.10g"
        CONVFMT="%.10g"

        is_first_command = """ + options["is_first_command"] + """
        is_last_command = """ + options["is_last_command"] + """
        
        
        delimiter_internal_notation = ":"
        if (FS == delimiter_internal_notation){
            delimiter_internal_notation = "#"
        }

        input_quote = \"""" + options["input_quote"] + """"
        output_quote = \"""" + options["output_quote"] + """"

        level_simplicity_csv = """ + options["level_simplicity_csv"] + """
        
        FS =\"""" + options["FS"] + """"
        
        OFS=\"""" + options["OFS"] + """"


        original_level_simplicity_csv = """ + options["original_level_simplicity_csv"] + """

        if (level_simplicity_csv <= 1){
            FPAT="([^" FS "]*)|(" input_quote "([^" input_quote "]|" input_quote input_quote ")+" input_quote ")"
        }


        records_skipped = 0

        minimal_string_quoting = """ + options["minimal_string_quoting"] + """
        full_string_quoting = !minimal_string_quoting

        is_unix_input = """ + options["is_unix_input"] + """
        is_unix_output = """ + options["is_unix_output"] + """

        if (is_unix_input){
        RS = "\\n"
        }else{
        RS = "\\r\\n"
        }

        if (is_unix_output){
        ORS = "\\n"
        }else{
        ORS = "\\r\\n"
        }
        null_input_string = \"""" + options["null_input_string"] + """"
        null_output_string = \"""" + options["null_output_string"] + """"

        header = """ + options["header"] + """
        output_header = """ + options["output_header"] + """

        if (!header){
            output_header = 0
        }

        add_index = """ + options["add_index"] + """
        index_based_on = """ + options["index_based_on"] + """

        line_based_code = """ + options["line_based_code"] + """
        fields_based_code = !line_based_code

        col_start = """ + options["col_start"] + """
        col_end = """ + options["col_end"] + """

        row_start = """ + options["row_start"] + """
        row_end = """ + options["row_end"] + """

        number_files_input = """ + options["number_files_input"] + """
        input_file_rows = """ + options["input_file_rows"] + """
        input_file_cols = !input_file_rows

        find_unique = """ + options["find_unique"] + """

        print_fields = """ + options["print_fields"] + """

        save = """ + options["save"] + """
        path_output = \"""" + options["path_output"] + """"

        sort = """ + options["sort"] + """
        sort_column = """ + options["sort_column"] + """
        num_cores = """ + options["num_cores"] + """
        sort_in_parallel = """ + options["sort_in_parallel"] + """

        calculate_shape = """ + options["calculate_shape"] + """

        check_complexity = """ + options["check_complexity"] + """

        add_new_column = """ + options["add_new_column"] + """
        name_new_column = \"""" + options["name_new_column"] + """"

        if (check_complexity){
            has_maximum_complexity = 0
            print_fields = 0
        }

        quotes_have_been_removed = 0
        number_fields = 0
        continue_next_line = 0
    }
    

    """
    return command


    



def body(level_simplicity_csv):
    command = ""
    debug("level_simplicity_csv",level_simplicity_csv,type(level_simplicity_csv))
    # if level_simplicity_csv == str(0):
    #     command = "!buildRec() { records_skipped += 1;next }"
        # command = "process_fields()"
    command = command + """
    {        
        if (!calculate_shape){
            
            if (check_complexity || number_files_input == 1){
                if (check_complexity){
                    if (line_number() == 0){
                        number_fields = max_col()
                        has_maximum_complexity = 0
                    }else{
                        if (max_col() < number_fields){
                            has_maximum_complexity = 1
                            exit
                        }
                    }
                }else{
                    if (line_number() == 0 && header){
                        # process_fields()
                        number_fields = NF
                        if (output_header){
                            print_header()
                        }
                    }else{
                        if (fields_based_code){
                            # process_fields()
                            if (line_number() >= row_start){
                                for (i=min_col();i<=max_col();i++) {                          
                                    if (condition()){                                
                                        print_field($i,i)
                                    }
                                }
                                i=min_col()
                                if (min_col() == max_col() && $i == ""){
                                    print(":n:")
                                }
                                add_column()
                            }
                        }else{              
                            # process_fields()              
                            if (line_number() >= row_start){
                            if (condition()){
                                print_line($0)                                
                            }

                            }
                        }
                        if (row_end != INF && line_number() > row_end){
                        exit
                        }
                    }
                }
            }else{
                if (FNR == NR){
                    v[$0] = 1

                }else{
                    if (FNR!=NR && FNR == 1){
                        records_skipped = 0
                    }
                    if (line_number() == 0 && header){
                        number_fields = max_col()
                        if (output_header){
                            print_header()
                        }
                    }else{
                        if (fields_based_code){
                            if (line_number() >= row_start){
                                for (i=min_col();i<=max_col();i++) {
                                if (condition()){
                                    field = $i
                                    if (input_file_rows && v[line_number()]){
                                        print_field(field,i)
                                    }else{
                                        if (input_file_cols && v[i]){
                                            print_field(field,i)
                                        }
                                    }
                                }
                                }
                                i=min_col()
                                if (min_col() == max_col() && $i == ""){
                                    print(":n:")
                                }
                                add_column()
                            }
                        }else{
                            if (line_number() >= row_start){
                            if (condition()){
                                if (input_file_rows && v[line_number()]){
                                    print_line($0)
                                }
                                
                            }

                            }
                        }
                        if (row_end != INF && line_number() > row_end){
                        exit
                        }
                    }
                }


            }
        }

    }

    """
    return command

def end():
    command = """
    END{
        if (find_unique){
            for (key in unique){
                print(key)
            }
        }
        if (calculate_shape){
            print print_line_number()
            print NF
        }
        if (check_complexity){
            print has_maximum_complexity
        }


    }
    """
    return command

def note(text,print_ = False):
    if print_:
        print(text)

def set_debug(on):
    os.environ["DEBUG"] = str(on)
    if on:
        set_now()

def is_debugging():
    return os.getenv("DEBUG") == "True"

def debug(*args):
    if is_debugging():
        try:
            elapsed_time = time.time() - float(os.getenv("NOW"))
            for text in args:
                print(text,sep=" ")
            print("time elapsed:", elapsed_time)                
            print("")
            set_now()
        except:
            for text in args:
                print(text,sep=" ")
            print("")

def set_now():
    if is_debugging():
        delete_now()
        os.environ["NOW"] = str(time.time())

def delete_now():
    if is_debugging():
        try:
            del os.environ['NOW']
        except:
            a = 1


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def output_quotes_around_string(string,quote = "\"",add_escape_character = False,escape_character = '\\',double_escape_character = False):
    if string != "":
        command = """gawk '{if ($0 ~ /^[\\\\+-]?[0-9]+$|^[\\\\+-]*[0-9]*[\\\\.]?[0-9]+$|^[\\\\+-]*[0-9]*[\\\\.]?[0-9]+[eE]?[\\\\+-]?[0-9]+$|^nan$|^Nan$|^NaN$|^NAN$/){print $0}else{print (\"""" + """" $0 \"""" + """")}}' <(echo '""" + string + "')"
        debug(command)
        result = subprocess.check_output(command, shell=True, executable='/bin/bash').decode()
        result = result.strip().split("\n")[0]
        debug("String to add quotes:",result)
        if result[0] == quote and add_escape_character:
            debug("adding escape character")
            if double_escape_character:
                result = escape_character + escape_character + escape_character + result[0:len(result)-1] + escape_character + escape_character + escape_character + quote  
            else:
                result = escape_character + result[0:len(result)-1] + escape_character + quote  
        debug("After adding quotes:",result)
        return result
    else:
        return string

def is_float(text):
    index = text.find(".")
    if index == -1:
        return False
    else:
        if index == len(text)-1:
            return is_int(text[0:index])
        elif index == 0:
            return is_int(text[index + 1:len(text)])
        else:
            return is_int(text[0:index]) and is_int(text[index + 1:len(text)])

def is_numeric(text):
    return is_int(text) or is_float(text)

def is_int(text):
    match = re.match(r'(^ *[\d]+ *$)|(^ *[\d]+([eE]?\d+)+$)',text)
    if match is not None and len(match.group().strip()) > 0:
        return True
    else:
        return False

def is_string(text):
    return not is_numeric(text)

    
#     if result == "True":
#         return True
#     else:
#         return False    


def find_first(object,target,starting_at = 0):
    i = starting_at
    for obj in object[starting_at:len(object)]:
        if obj == target:
            return i
        i += 1
    return None




class Conditional_equation:
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)
    def __init__(self):
        super(Conditional_equation, self).__setattr__('condition', True)
        super(Conditional_equation, self).__setattr__('equation', "")
        super(Conditional_equation, self).__setattr__('__columns__', [])
        super(Conditional_equation, self).__setattr__('__delimiter__', ",")
        super(Conditional_equation, self).__setattr__('__string_delimiter__', "\"")
        super(Conditional_equation, self).__setattr__('__floating_precision__', "0.00000000000001")
        # super(Conditional_equation, self).__setattr__('__floating_precision__', "1e-10")
        super(Conditional_equation, self).__setattr__('__verbose__', True)

    def __getattr__(self, name):
        return super(Conditional_equation, self).__getattr__(name)
    def __setattr__(self, name, value):
        if name == "equation":
            set_now()
            equation = value.replace(" in ["," _in_ [")
            equation = value.replace(" in ["," _in_ [")
            operators = ["=","\\\\(","\\\\)","\\\\+","-","\\\\*\\\\*","\\\\*","/","\\\\^"]
            operators.extend([">=","<=",">","<","==","!=","~","&&","\\\\|\\\\|","&","\\\\|","!","\\\\(","\\\\)","\\\\[","\\\\]"])
            operator = np.unique(operators)
            operator_str = ""
            for op in operators:
                operator_str += "([" + op + "])+"
                if op != operators[len(operators)-1]:
                    operator_str += "|"
            debug("operators",operator_str)

            is_digit_regex = """^[\\\\+-]?[0-9]+$|^[\\\\+-]*[0-9]*[\\\\.]?[0-9]+$|^[\\\\+-]*[0-9]*[\\\\.]?[0-9]+[eE]?[\\\\+-]?[0-9]+$|^nan$|^Nan$|^NaN$|^NAN$"""
            fpat = operator_str + "|" + is_digit_regex + "|([a-zA-Z0-9][_-]*)+||(_in_)+|(\"([^\"]|\"\")+\")"
            command = """gawk -v FPAT='""" + fpat + """' 'BEGIN{}{for (i=1;i<NF;i++){print($i)}};{print($NF)}' <(echo '""" + equation + """')"""
            # command += " <(" + condition + ")"
            result = subprocess.check_output(command, shell=True, executable='/bin/bash').decode()


            elements = result.split("\n")            
            elements = [x for x in elements if x != ""]

            strings_in_quotes = []
            for string_ in elements:
                if string_[0] == "\"" and string_[len(string_)-1] == "\"":
                    strings_in_quotes.append(string_)
            debug("Strings in quotes",strings_in_quotes)
            str_dict = {}
            for string_ in strings_in_quotes:
                str_dict[string_] = get_random_string(20).replace(" ","").replace("(","").replace(")","")

            elements_dict = {}
            i = 0
            for elem in elements:
                if elem in elements_dict.keys():
                    elements_dict[elem].append(i)
                else:
                    elements_dict[elem] = [i]
                i += 1

            for string_ in strings_in_quotes:
                counter = 0
                while string_ in elements and counter < 100:
                    counter += 1
                    for index in elements_dict[string_]:
                        elements[index] = str_dict[string_]
                    # print(equation)

            # indices_in = []
            # for i in range(len(elements)):
            #     if elements[i] == "_in_":
            #         indices_in.append(i)
            # print(indices_in)

            new_elements = []
            index = 0
            skip = []
            for elem in elements:
                if elem =="_in_":
                    variable = elements[index - 1]
                    index_left_bracket = index + 1
                    index_right_bracket = find_first(elements,"]",index)
                    for j in range(index,index_right_bracket + 1):
                        skip.append(j)
                    new_elements.append("(")
                    for j in range(index + 2,index_right_bracket):
                        # new_elements.append("(")
                        if not is_float(elements[j]):
                            new_elements.append(variable)
                            new_elements.append("==")
                            new_elements.append(elements[j])
                        else:
                            new_elements.append("(")
                            new_elements.append(variable)
                            new_elements.append(">=")
                            new_elements.append(elements[j] + " - " + (self.__floating_precision__))
                            new_elements.append("&&")
                            new_elements.append(variable)
                            new_elements.append("<=")
                            new_elements.append(elements[j] + " + " + (self.__floating_precision__))
                            new_elements.append(")")
                        # new_elements.append(")")
                        if j != index_right_bracket - 1:
                            new_elements.append("||")

                    new_elements.append(")")
                elif elem == "==" and is_float(elements[index + 1]):                    
                    
                    variable = elements[index - 1]
                    value = elements[index + 1]
                    for j in range(index,index + 2):
                        skip.append(j)
                    new_elements.append("(")
                    new_elements.append(variable)
                    new_elements.append(">=" )
                    new_elements.append(value + "-" + (self.__floating_precision__))
                    new_elements.append("&&")
                    new_elements.append(variable)
                    new_elements.append("<=" )
                    new_elements.append(value + "+" + (self.__floating_precision__))
                    new_elements.append(")")
                if index not in skip and index == len(elements) - 1:
                    new_elements.append(elem)
                # elif index not in skip and (elements[index + 1] != "_in_"):
                elif index not in skip and (elements[index + 1] != "_in_" and not (elements[index + 1] == "==" and is_float(elements[index + 2]))):
                    new_elements.append(elem)
                    
                index += 1

            elements = new_elements
            # for index in indices_in:
            #     index_left_bracket = index + 1
            #     index_right_bracket = find_first(elements,"]",index)
            #     new_text = "("
            #     variable = elements[index-1]
            #     data = elements[index+1]
            #     data = data.replace("[","").replace("]","")
            #     data = data.split(",")
            #     for d in data:
            #         new_text = new_text + variable + "==" + d
            #         if d != data[len(data)-1]:
            #             new_text += "|"
            #         else:
            #             new_text += ")"
            #     elements[index] = ""
            #     elements[index + 1] = ""
            #     elements[index-1] = new_text
            equation = " ".join(elements)

            names = self.__columns__
            lengths = [len(x) for x in names]
            order = np.argsort(-np.array(lengths))
            names = names[order]
            # print(names)
            for i in range(len(names)):
                equation = equation.replace(names[i],"$" + str(order[i]+1))
            bit_operators_and_or_not = ["&","|","!"]
            awk_operators_and_or_not = ["&&","||","!"]
            

            for i in range(len(bit_operators_and_or_not)):
                equation = equation.replace(awk_operators_and_or_not[i],bit_operators_and_or_not[i])

            for i in range(len(bit_operators_and_or_not)):
                equation = equation.replace(bit_operators_and_or_not[i],awk_operators_and_or_not[i])
            
            

            # awk_command_ = Awk_command()
            # awk_command_.options = get_options_default()
            # awk_command_.options["header"] = "0"
            # # awk_command_.options["level_simplicity_csv"] = str(self.)
            # awk_command_.commands = get_default_commands()
            # awk_command_.priority = 9999999999
            # awk_command_.type = "equation"
            # awk_command_.persistance_in_time = "instance"
            # awk_command_to_file(awk_command_)
            output_str = {}
            for k in str_dict.keys():
                k_0 = deepcopy(k)
                # if k[0] == "\"":
                #     k = k[1:]
                # if k[len(k)-1] =="\"":
                #     k = k[:len(k)-1]
                # command = "gawk -f " + awk_command_.path_execution_file + " <(echo '\"" + k + "\"')"
                # result = subprocess.check_output(command, shell=True, executable='/bin/bash').decode()
                # result = result.strip()
                output_str[str_dict[k_0]] = k_0
            for k in output_str.keys():
                string_ = k
                while string_ in equation:
                    equation = equation.replace(string_,output_str[string_])
            debug("equation",equation)

            elements = re.findall(r'== \"[^|&]*\"',equation)
            old_elems = []
            new_elems = []
            for elem in elements:
                old_elems.append(deepcopy(elem))
                
                
                elem = elem.replace('(','\\(')
                elem = elem.replace(')','\\)')
                elem = elem.replace('[','\\[')
                elem = elem.replace(']','\\]')
                elem = elem.replace('/','\\/')
                elem = elem.replace('$','\\$')
                elem = elem.replace('^','\\^')
                elem = elem.replace('.','\\.')
                elem = elem.replace('|','\\|')
                elem = elem.replace('*','\\*')
                elem = elem.replace('+','\\+')
                elem = elem.replace('?','\\?')


                elem = elem.replace('"','"?')
                elem = elem.replace('== ','~ ')
                elem = elem.replace('~ ','~ /^')

                #here, only if previous command transformed the input
                elem = elem.replace(',',':d:')
                elem = elem.replace('\"',':q:')
                elem = elem.replace('\\n',':n:')
                elem = elem.replace('\\r',':r:')
                elem += '$/'
                elem = elem.replace('/^:q:','/^"')
                elem = elem.replace(':q:?$/','\"?$/')
                
                
                new_elems.append(elem)
            for i in range(len(old_elems)):
                counter = 0
                while old_elems[i] in equation and counter < 100:
                    counter += 1
                    equation = equation.replace(old_elems[i],new_elems[i])
                if counter > 75:
                    print("Something strange happenned with the equation ",equation)

            elements = re.findall(r'!= \"[^|&]*\"',condition)
            old_elems = []
            new_elems = []
            for elem in elements:
                old_elems.append(deepcopy(elem))
                
                
                elem = elem.replace('(','\\(')
                elem = elem.replace(')','\\)')
                elem = elem.replace('[','\\[')
                elem = elem.replace(']','\\]')
                elem = elem.replace('/','\\/')
                elem = elem.replace('$','\\$')
                elem = elem.replace('^','\\^')
                elem = elem.replace('.','\\.')
                elem = elem.replace('|','\\|')
                elem = elem.replace('*','\\*')
                elem = elem.replace('+','\\+')
                elem = elem.replace('?','\\?')


                elem = elem.replace('"','"?')
                elem = elem.replace('!= ','!~ ')
                elem = elem.replace('~ ','~ /^')

                #here, only if previous command transformed the input
                elem = elem.replace(',',':d:')
                elem = elem.replace('\"',':q:')
                elem = elem.replace('\\n',':n:')
                elem = elem.replace('\\r',':r:')
                elem += '$/'
                elem = elem.replace('/^:q:','/^"')
                elem = elem.replace(':q:?$/','\"?$/')
                
                
                new_elems.append(elem)
            
            for i in range(len(old_elems)):
                counter = 0
                while old_elems[i] in condition and counter < 100:
                    counter += 1
                    condition = condition.replace(old_elems[i],new_elems[i])
                if counter > 75:
                    print("Something strange happenned with the condition ",condition)

            
            debug("Final equation:",equation)
            if self.__verbose__:
                print("Executing equation:\n",equation)
            
            elements = equation.split("=")
            equation = "if (column == " + elements[0].replace("$","") + "){field = " + elements[1] + "}" 


            value = equation
            delete_now()



        if name == "condition":
            set_now()
            condition = value.replace(" in ["," _in_ [")
            condition = value.replace(" in ["," _in_ [")
            operators = [">=","<=",">","<","==","!=","~","&&","\\\\|\\\\|","&","\\\\|","!","\\\\(","\\\\)","\\\\[","\\\\]"]
            operator_str = ""
            for op in operators:
                operator_str += "([" + op + "])+"
                if op != operators[len(operators)-1]:
                    operator_str += "|"
            debug("operators",operator_str)

            is_digit_regex = """^[\\\\+-]?[0-9]+$|^[\\\\+-]*[0-9]*[\\\\.]?[0-9]+$|^[\\\\+-]*[0-9]*[\\\\.]?[0-9]+[eE]?[\\\\+-]?[0-9]+$|^nan$|^Nan$|^NaN$|^NAN$"""
            fpat = operator_str + "|" + is_digit_regex + "|([a-zA-Z0-9][_-]*)+||(_in_)+|(\"([^\"]|\"\")+\")"
            command = """gawk -v FPAT='""" + fpat + """' 'BEGIN{}{for (i=1;i<NF;i++){print($i)}};{print($NF)}' <(echo '""" + condition + """')"""
            # command += " <(" + condition + ")"
            result = subprocess.check_output(command, shell=True, executable='/bin/bash').decode()


            elements = result.split("\n")            
            elements = [x for x in elements if x != ""]

            strings_in_quotes = []
            for string_ in elements:
                if string_[0] == "\"" and string_[len(string_)-1] == "\"":
                    strings_in_quotes.append(string_)
            debug("Strings in quotes",strings_in_quotes)
            str_dict = {}
            for string_ in strings_in_quotes:
                str_dict[string_] = get_random_string(20).replace(" ","").replace("(","").replace(")","")

            elements_dict = {}
            i = 0
            for elem in elements:
                if elem in elements_dict.keys():
                    elements_dict[elem].append(i)
                else:
                    elements_dict[elem] = [i]
                i += 1

            for string_ in strings_in_quotes:
                counter = 0
                while string_ in elements and counter < 100:
                    counter += 1
                    for index in elements_dict[string_]:
                        elements[index] = str_dict[string_]
                    # print(condition)

            # indices_in = []
            # for i in range(len(elements)):
            #     if elements[i] == "_in_":
            #         indices_in.append(i)
            # print(indices_in)

            new_elements = []
            index = 0
            skip = []
            for elem in elements:
                if elem =="_in_":
                    variable = elements[index - 1]
                    index_left_bracket = index + 1
                    index_right_bracket = find_first(elements,"]",index)
                    for j in range(index,index_right_bracket + 1):
                        skip.append(j)
                    new_elements.append("(")
                    for j in range(index + 2,index_right_bracket):
                        # new_elements.append("(")
                        if not is_float(elements[j]):
                            new_elements.append(variable)
                            new_elements.append("==")
                            new_elements.append(elements[j])
                        else:
                            new_elements.append("(")
                            new_elements.append(variable)
                            new_elements.append(">=")
                            new_elements.append(elements[j] + " - " + (self.__floating_precision__))
                            new_elements.append("&&")
                            new_elements.append(variable)
                            new_elements.append("<=")
                            new_elements.append(elements[j] + " + " + (self.__floating_precision__))
                            new_elements.append(")")
                        # new_elements.append(")")
                        if j != index_right_bracket - 1:
                            new_elements.append("||")

                    new_elements.append(")")
                elif elem == "==" and is_float(elements[index + 1]):                    
                    
                    variable = elements[index - 1]
                    value = elements[index + 1]
                    for j in range(index,index + 2):
                        skip.append(j)
                    new_elements.append("(")
                    new_elements.append(variable)
                    new_elements.append(">=" )
                    new_elements.append(value + "-" + (self.__floating_precision__))
                    new_elements.append("&&")
                    new_elements.append(variable)
                    new_elements.append("<=" )
                    new_elements.append(value + "+" + (self.__floating_precision__))
                    new_elements.append(")")
                if index not in skip and index == len(elements) - 1:
                    new_elements.append(elem)
                # elif index not in skip and (elements[index + 1] != "_in_"):
                elif index not in skip and (elements[index + 1] != "_in_" and not (elements[index + 1] == "=="  and is_float(elements[index + 2]))):
                    new_elements.append(elem)
                    
                index += 1

            elements = new_elements
            # for index in indices_in:
            #     index_left_bracket = index + 1
            #     index_right_bracket = find_first(elements,"]",index)
            #     new_text = "("
            #     variable = elements[index-1]
            #     data = elements[index+1]
            #     data = data.replace("[","").replace("]","")
            #     data = data.split(",")
            #     for d in data:
            #         new_text = new_text + variable + "==" + d
            #         if d != data[len(data)-1]:
            #             new_text += "|"
            #         else:
            #             new_text += ")"
            #     elements[index] = ""
            #     elements[index + 1] = ""
            #     elements[index-1] = new_text
            condition = " ".join(elements)

            names = self.__columns__
            lengths = [len(x) for x in names]
            order = np.argsort(-np.array(lengths))
            names = names[order]
            # print(names)

            for i in range(len(names)):
                condition = condition.replace(names[i],"$" + str(order[i]+1))
            # print(names)
            bit_operators_and_or_not = ["&","|","!"]
            awk_operators_and_or_not = ["&&","||","!"]


            for i in range(len(bit_operators_and_or_not)):
                condition = condition.replace(awk_operators_and_or_not[i],bit_operators_and_or_not[i])

            for i in range(len(bit_operators_and_or_not)):
                condition = condition.replace(bit_operators_and_or_not[i],awk_operators_and_or_not[i])
            
            

            # awk_command_ = Awk_command()
            # awk_command_.options = get_options_default()
            # awk_command_.options["header"] = "0"
            # # awk_command_.options["level_simplicity_csv"] = str(self.)
            # awk_command_.commands = get_default_commands()
            # awk_command_.priority = 9999999999
            # awk_command_.type = "condition"
            # awk_command_.persistance_in_time = "instance"
            # awk_command_to_file(awk_command_)
            output_str = {}
            for k in str_dict.keys():
                k_0 = deepcopy(k)
                # if k[0] == "\"":
                #     k = k[1:]
                # if k[len(k)-1] =="\"":
                #     k = k[:len(k)-1]
                # command = "gawk -f " + awk_command_.path_execution_file + " <(echo '\"" + k + "\"')"
                # result = subprocess.check_output(command, shell=True, executable='/bin/bash').decode()
                # result = result.strip()
                output_str[str_dict[k_0]] = k_0
            for k in output_str.keys():
                string_ = k
                while string_ in condition:
                    condition = condition.replace(string_,output_str[string_])
            debug("Condition",condition)



            elements = re.findall(r'== \"[^|&]*\"',condition)
            old_elems = []
            new_elems = []
            for elem in elements:
                old_elems.append(deepcopy(elem))
                
                
                elem = elem.replace('(','\\(')
                elem = elem.replace(')','\\)')
                elem = elem.replace('[','\\[')
                elem = elem.replace(']','\\]')
                elem = elem.replace('/','\\/')
                elem = elem.replace('$','\\$')
                elem = elem.replace('^','\\^')
                elem = elem.replace('.','\\.')
                elem = elem.replace('|','\\|')
                elem = elem.replace('*','\\*')
                elem = elem.replace('+','\\+')
                elem = elem.replace('?','\\?')


                elem = elem.replace('"','"?')
                elem = elem.replace('== ','~ ')
                elem = elem.replace('~ ','~ /^')

                #here, only if previous command transformed the input
                elem = elem.replace(',',':d:')
                elem = elem.replace('\"',':q:')
                elem = elem.replace('\\n',':n:')
                elem = elem.replace('\\r',':r:')
                elem += '$/'
                elem = elem.replace('/^:q:','/^"')
                elem = elem.replace(':q:?$/','\"?$/')
                
                
                new_elems.append(elem)
            
            for i in range(len(old_elems)):
                counter = 0
                while old_elems[i] in condition and counter < 100:
                    counter += 1
                    condition = condition.replace(old_elems[i],new_elems[i])
                if counter > 75:
                    print("Something strange happenned with the condition ",condition)


            elements = re.findall(r'!= \"[^|&]*\"',condition)
            old_elems = []
            new_elems = []
            for elem in elements:
                old_elems.append(deepcopy(elem))
                
                
                elem = elem.replace('(','\\(')
                elem = elem.replace(')','\\)')
                elem = elem.replace('[','\\[')
                elem = elem.replace(']','\\]')
                elem = elem.replace('/','\\/')
                elem = elem.replace('$','\\$')
                elem = elem.replace('^','\\^')
                elem = elem.replace('.','\\.')
                elem = elem.replace('|','\\|')
                elem = elem.replace('*','\\*')
                elem = elem.replace('+','\\+')
                elem = elem.replace('?','\\?')


                elem = elem.replace('"','"?')
                elem = elem.replace('!= ','!~ ')
                elem = elem.replace('~ ','~ /^')

                #here, only if previous command transformed the input
                elem = elem.replace(',',':d:')
                elem = elem.replace('\"',':q:')
                elem = elem.replace('\\n',':n:')
                elem = elem.replace('\\r',':r:')
                elem += '$/'
                elem = elem.replace('/^:q:','/^"')
                elem = elem.replace(':q:?$/','\"?$/')
                
                
                new_elems.append(elem)
            
            for i in range(len(old_elems)):
                counter = 0
                while old_elems[i] in condition and counter < 100:
                    counter += 1
                    condition = condition.replace(old_elems[i],new_elems[i])
                if counter > 75:
                    print("Something strange happenned with the condition ",condition)
            

            
            debug("Final condition:",condition)
            if self.__verbose__:
                print("Executing condition:\n",condition)

            value = condition
            delete_now()

        super(Conditional_equation, self).__setattr__(name, value)


class Awk_command:
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)
    def __init__(self):
        super(Awk_command, self).__setattr__('commands', {})
        super(Awk_command, self).__setattr__('priority', 3)
        super(Awk_command, self).__setattr__('type', "")
        super(Awk_command, self).__setattr__('persistance_in_time', "continuous")
        super(Awk_command, self).__setattr__('persistance_after_execution', "ephemeral")
        super(Awk_command, self).__setattr__('id', get_random_string(20))
        super(Awk_command, self).__setattr__('path_temp_file', "")
        super(Awk_command, self).__setattr__('path_execution_file', "")
        super(Awk_command, self).__setattr__('options', {})


    def __getattr__(self, name):
        return super(Awk_command, self).__getattr__(name)
    def __setattr__(self, name, value):
        super(Awk_command, self).__setattr__(name, value)


    def __copy__(self):
        cls = self.__class__
        com = cls.__new__(cls)
        com.__dict__.update(self.__dict__)
        self.has_been_copied = True
        com.has_been_copied = True
        return com

    def __deepcopy__(self,memo):
        cls = self.__class__
        com = cls.__new__(cls)
        memo[id(self)] = com
        for k, v in self.__dict__.items():
            setattr(com, k, deepcopy(v, memo))

        # com = Awk_command()
        # com.command = self.command
        # com.priority = self.priority
        # com.type = self.type
        # com.persistance_in_time = self.persistance_in_time
        # com.persistance_after_execution = self.persistance_after_execution
        # com.id = self.id
        # com.output_header = self.output_header
        # com.has_header = self.has_header
        # com.nrow_selected = self.nrow_selected
        # com.ncol_selected = self.ncol_selected
        # com.nrow_before = self.nrow_before
        # com.ncol_before = self.ncol_before
        return com

def get_default_commands():
    commands = {}
    commands["commands_transform_column"]=""
    commands["commands_transform_digit"]=""
    commands["command_transform_string"]=""
    commands["command_transform_line"]=""
    commands["command_condition"]=""
    return commands    

def compose_generic_command(options,commands_transform_column="",commands_transform_digit="",command_transform_string="",command_transform_line="",command_condition=""):    
    
    text = generic_functions_awk()
    text += function_transform_column(commands = commands_transform_column)
    text += function_transform_digit(commands = commands_transform_digit)
    text += function_transform_string(commands = command_transform_string)
    text += function_transform_line(commands = command_transform_line)
    text += function_condition(commands = command_condition)
    text += begin(options)
    text += body(options["level_simplicity_csv"])
    text += end()
    return text



class DataFrame:
    # __names_attributes__ = ["__path__","__has_header__","__commands__","__delimiter__","__id__","__ncol__","__nrow__","__ncol_original__","__nrow_original__","__columns__","__selected_columns__","__nrow_modified_to_unknown_value__"]
    def __repr__(self):
        text = self.head(n = self.__max_lines_print__).execute()
        self.__max_lines_print__ = self.__max_lines_print_original__
        return text
    def __str__(self):
        text = self.head(n = self.__max_lines_print__).execute()
        self.__max_lines_print__ = self.__max_lines_print_original__
        return text
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)
    def __init__(self):
        super(DataFrame, self).__setattr__('__path__', "")
        super(DataFrame, self).__setattr__('__has_header__',True)
        super(DataFrame, self).__setattr__('__commands__', [])
        super(DataFrame, self).__setattr__('__num_copies_commands__', {})
        super(DataFrame, self).__setattr__('__delimiter__', ",")
        super(DataFrame, self).__setattr__('__id__', get_random_string(20))
        super(DataFrame, self).__setattr__('__ncol__', 0)
        super(DataFrame, self).__setattr__('__nrow__', 0)
        super(DataFrame, self).__setattr__('__ncol_original__', 0)
        super(DataFrame, self).__setattr__('__nrow_original__', 0)
        super(DataFrame, self).__setattr__('__columns__', [])
        super(DataFrame, self).__setattr__('__selected_columns__', [])
        super(DataFrame, self).__setattr__('__nrow_modified_to_unknown_value__', True)
        super(DataFrame, self).__setattr__('__string_delimiter__', "\"")
        super(DataFrame, self).__setattr__('__columns_changed__', False)
        super(DataFrame, self).__setattr__('__level_simplicity_csv__', 0)
        super(DataFrame, self).__setattr__('__version__', "0_2_3")
        super(DataFrame, self).__setattr__('__max_lines_print__', 200)
        super(DataFrame, self).__setattr__('__max_lines_print_original__', 200)
        


    # def __copy__(self):
    #     cls = self.__class__
    #     result = cls.__new__(cls)
    #     result.__dict__.update(self.__dict__)
    #     return result
    #     # print(type(self))
    #     # print(super(DataFrame, self))
    #     # __ddf_new__ = DataFrame()
    #     # for name in DataFrame.__names_attributes__:
    #     #     # super(DataFrame, __ddf_new__).__setattr__(name,super(DataFrame, self).__getattr__(name))
    #     #     __ddf_new__.__setattr__(name,self.__getattr__(name))
    #     # __ddf_new__.commands = []
    #     # # __ddf_new__.__ncol__ = __ddf_new__.__ncol_original__
    #     # # __ddf_new__.__nrow__ = __ddf_new__.__ncol_original__
    #     # for command in self.__commands__:
    #     #     com = command.___copy__()
    #     #     __ddf_new__.commands.append(com)
    #     # return __ddf_new__

    def __del__(self):
        for command in self.__commands__:
            self.__num_copies_commands__[command.id] -= 1
        self.__clear_all_commands__()



    def __deepcopy_internal__(self,memo):
        # cls = self.__class__
        # result = cls.__new__(cls)
        # memo[id(self)] = result
        # for k, v in self.__dict__.items():
        #     setattr(result, k, deepcopy(v, memo))


    #

        __ddf_new__ = DataFrame()
        # __names_attributes__ = ['__path__',"__has_header__","__commands__","__delimiter__","__id__","__ncol__","__nrow__","__ncol_original__","__nrow_original__","__columns__","__selected_columns__","__nrow_modified_to_unknown_value__"]
        # for name in __names_attributes__:
        #     print(name)
        #     # super(DataFrame, __ddf_new__).__setattr__(name,super(DataFrame, self).__getattr__(name))
        #     # __ddf_new__.__setattr__(name,self.__getattr__(name))
        #     __ddf_new__.name = DataFrame.__getattr__(self,name)
        __ddf_new__.__path__ = self.__path__
        __ddf_new__.__has_header__ = self.__has_header__
        __ddf_new__.__num_copies_commands__ = self.__num_copies_commands__
        __ddf_new__.__delimiter__ = self.__delimiter__
        # __ddf_new__.__id__ = self.__id__
        __ddf_new__.__ncol__ = self.__ncol__
        __ddf_new__.__nrow__ = self.__nrow__
        __ddf_new__.__ncol_original__ = self.__ncol_original__
        __ddf_new__.__nrow_original__ = self.__nrow_original__
        __ddf_new__.__columns__ = self.__columns__
        __ddf_new__.__selected_columns__ = self.__selected_columns__
        __ddf_new__.__nrow_modified_to_unknown_value__ = self.__nrow_modified_to_unknown_value__
        __ddf_new__.__string_delimiter__ = self.__string_delimiter__
        __ddf_new__.__columns_changed__ = self.__columns_changed__
        __ddf_new__.__level_simplicity_csv__= self.__level_simplicity_csv__

        # __ddf_new__.__commands__ = []
        # __ddf_new__.__ncol__ = __ddf_new__.__ncol_original__
        # __ddf_new__.__nrow__ = __ddf_new__.__ncol_original__
        for command in self.__commands__:
            # com = command.___copy__()
            com = deepcopy(command)
            if command.id not in __ddf_new__.__num_copies_commands__.keys():
                __ddf_new__.__num_copies_commands__[command.id] = 0
            __ddf_new__.__num_copies_commands__[command.id] += 1
            __ddf_new__.__commands__.append(com)
        return __ddf_new__

    def __getattr__(self, name):
        # print(name)
        # print(DataFrame.__names_attributes__)
        # if name in DataFrame.__names_attributes__:
        try:
            return super(DataFrame, self).__getattr__(name)            
        except:
        # else:
            # if name == ""
            debug("calling names in __getattr__",self.__columns_changed__)
            if name in self.names():
                __ddf__ = self.get_cols([name])
                # t = __ddf__.to_npd()
                return __ddf__
            else:
                raise Exception("Column not found")

    def __setattr__(self, name, value):
        # if name != "__names_attributes__":
        # if name in DataFrame.__names_attributes__:
        try:
            super(DataFrame, self).__setattr__(name, value)
        except:
            note("First needs to implement set_rows(rows,Xs)")
        # else:
        #     names = self.names()
        #     if name in names:
        #         print("not yet")


#         if type(value) == list:
#             value = np.array(value)
#         self.d[name] = value
#         super(DataFrame, self).__setattr__('ncol', self.__ncol__ + 1)
#         if self.__nrow__ == 0:
#             super(DataFrame, self).__setattr__('nrow', len(value))
    def __getitem__(self,args):
        debug(type(args))
        note("TODO: make another global variable that keeps tracks of current names and use it here and in other column selection options to warn")
        if type(args) == tuple:
            rows,cols=args
            if type(rows) == int:
                rows = [rows]
            if type(cols) == int:
                cols = [cols]

            return self.get_rows(rows).get_cols(cols)
        else:
            cols = args
            if type(cols) == int:
                cols = [cols]
            return self.get_cols(cols)
    #     print("not yet")
#         if type(args) == tuple:

#             if len(key) == 1:
#                 if type(key) == list:
#                     t_ = DataFrame()
#                     for k in key:
#                         DataFrame.__setattr__(t_,k,self.d[k][rows])
#                     return t_
#                 else:
#                     __ddf__ = self.__deepcopy_internal__({})
# __ddf__.__settle_commands__()
# self.__clear_commands__()
# return __ddf__.d[key][rows]
#             else:
#                 t_ = DataFrame()
#                 for k in key:
#                     DataFrame.__setattr__(t_,k,self.d[k][rows])
#                 return t_
#         else:
#             key = args
#             if type(key) == str:
#                 __ddf__ = self.__deepcopy_internal__({})
# __ddf__.__settle_commands__()
# self.__clear_commands__()
# return __ddf__.d[key]
#             else:
#                 if len(key) == 1:
#                     if type(key) == list:
#                         t_ = DataFrame()
#                         for k in key:
#                             DataFrame.__setattr__(t_,k,self.d[k])
#                         return t_
#                     else:
#                         __ddf__ = self.__deepcopy_internal__({})
# __ddf__.__settle_commands__()
# self.__clear_commands__()
# return __ddf__.d[key]
#                 else:
#                     t_ = DataFrame()
#                     for k in key:
#                         DataFrame.__setattr__(t_,k,self.d[k])
#                     return t_

    # def __setitem__(self,key,values):
    #     print("not yet")
#         DataFrame.__setattr__(self,key,values)

    def read_csv(self,path,delimiter = ",",has_header = True,string_delimiter = "\"",names_columns = [],fields_may_contain_delimiter = True,fields_may_contain_line_breaks = True):

        if os.path.exists(path):
            if string_delimiter == '"':
                string_delimiter = "\""
            self.__string_delimiter__ = string_delimiter
            self.__path__ = path
            self.__delimiter__ = delimiter
            self.__has_header__ = has_header
            self.__columns_changed__ = True
            debug("Value line breaks is None",fields_may_contain_line_breaks is None)
            debug("Value line breaks",fields_may_contain_line_breaks)
            debug("Value delimiter in string",fields_may_contain_delimiter)
            if fields_may_contain_line_breaks is None:

                awk_command = Awk_command()
                awk_command.options = get_options_default()
                awk_command.options["print_fields"] = "0"
                awk_command.options["output_header"] = "0"
                awk_command.options["check_complexity"] = "1"
                awk_command.options["line_based_code"] = "0"
                if fields_may_contain_delimiter:
                    self.__level_simplicity_csv__ = 1
                else:
                    self.__level_simplicity_csv__ = 2
                awk_command.commands = get_default_commands()

                # awk_command.command = command
                awk_command.priority = 9999999999
                awk_command.type = "check_complexity"
                awk_command.persistance_in_time = "instance"
                self.__commands__.append(awk_command)
                id_command = awk_command.id
                if id_command not in self.__num_copies_commands__.keys():
                    self.__num_copies_commands__[id_command] = 0
                self.__num_copies_commands__[id_command] += 1
                result = self.execute()
                if result.strip().replace("\n","") == "1":
                    debug("has maximum complexity")
                    self.__level_simplicity_csv__ = 0
            else:
                debug("in here")
                if (fields_may_contain_delimiter and fields_may_contain_line_breaks):
                    self.__level_simplicity_csv__ = 0
                elif (fields_may_contain_line_breaks):
                    self.__level_simplicity_csv__ = 0
                elif (fields_may_contain_delimiter):
                    self.__level_simplicity_csv__ = 1
                else:
                    self.__level_simplicity_csv__ = 2
            
            self.names()
            debug("level simplicity in read",self.__level_simplicity_csv__)
            # self.shape()
        else:
            raise Exception("File name does not exists")

    def shape(self):
        if self.__ncol_original__ == 0 or self.__nrow_original__ == 0:
#             command = "wc -l " + self.__path__
#             result = subprocess.check_output(command, shell=True, executable='/bin/bash').decode()
#             values = result.replace("\n","").strip().split(" ")[0]
#             nrow = int(values)
#             if self.__has_header__:
#                 nrow -= 1

#             # command = "gawk -v FPAT='([^" + self.__delimiter__ + "]*)|(" + self.__string_delimiter__ + "[^" + self.__string_delimiter__ + "]+" + self.__string_delimiter__ + ")' 'BEGIN{}{if (NR>1){exit}}END{print NF}' " + self.__path__
# #             print(command)
#             # result = subprocess.check_output(command, shell=True, executable='/bin/bash').decode()
#             names = self.names()

#             values = len(names)
#             ncol = values
#             values = np.array([nrow,ncol]).astype(int)
#             self.__ncol__ = values[1]
#             self.__nrow__ = values[0]
#             self.__ncol_original__ = ncol
#             self.__nrow_original__ = nrow
#             self.__clear_commands__()
#             return values

            shape = self.__shape_current__().execute()
            
            # debug(shape)
            values = shape.split("\n")
            values = [x for x in values if x != ""]
            values = np.array(values).astype(int)
#                 self.__nrow_modified_to_unknown_value__ = False
            # self.__ncol__ = values[1]
            # self.__nrow__ = values[0]
            self.__ncol_original__ = values[1]
            self.__nrow_original__ = values[0]
            return values
        else:
            shape = self.__shape_current__().execute()
            
            # debug(shape)
            values = shape.split("\n")
            values = [x for x in values if x != ""]
            values = np.array(values).astype(int)
#                 self.__nrow_modified_to_unknown_value__ = False
            # self.__ncol__ = values[1]
            # self.__nrow__ = values[0]
            self.__ncol_original__ = values[1]
            self.__nrow_original__ = values[0]
            return values


    def __shape_current__(self,has_header = True):
        # command = "gawk -v FPAT='([^" + self.__delimiter__ + "]*)|(" + self.__string_delimiter__ + "[^" + self.__string_delimiter__ + "]+" + self.__string_delimiter__ + ")' -v has_header=has_header_variable " + """'
        # BEGIN {

        #     number_rows = 0
        # }
        # {
        #     if (NR == 1){
        #         if (has_header){
        #         }else{
        #             number_rows+=1
        #         }

        #     }else{
        #         number_rows+=1

        #     }
        # }
        # END {
        #     printf("%s""" + self.__delimiter__ + """",number_rows)
        #     print(NF)
        # }
        # ' """

        awk_command = Awk_command()
        awk_command.options = get_options_default()
        awk_command.options["print_fields"] = "0"
        awk_command.options["output_header"] = "0"
        awk_command.options["calculate_shape"] = "1"
        awk_command.options["line_based_code"] = "0"
        awk_command.commands = get_default_commands()

        # awk_command.command = command
        awk_command.priority = 9999999999
        awk_command.type = "shape"
        awk_command.persistance_in_time = "instance"
        self.__commands__.append(awk_command)
        id_command = awk_command.id
        if id_command not in self.__num_copies_commands__.keys():
            self.__num_copies_commands__[id_command] = 0
        self.__num_copies_commands__[id_command] += 1
        return self



    def names(self):
        debug(self.__columns_changed__)
        if self.__columns_changed__:
            if self.__has_header__:                
            #     command = "gawk -v FPAT='([^" + self.__delimiter__ + "]*)|(" + self.__string_delimiter__ + "[^" + self.__string_delimiter__ + "]+" + self.__string_delimiter__ + ")' " + """'
            # BEGIN {

            # }
            # {
            #     if (NR == 1){
            #         print
            #         exit
            #     }
            # }
            # END {}
            # ' """ 

                awk_command = Awk_command()
                awk_command.options = get_options_default()
                awk_command.options["print_fields"] = "0"
                awk_command.options["row_end"] = "1"
                awk_command.options["line_based_code"] = "0"
                awk_command.commands = get_default_commands()
                awk_command.priority = 9999999999
                awk_command.type = "names"
                awk_command.persistance_in_time = "instance"
                # self.__commands__.insert(0,awk_command)
                self.__commands__.append(awk_command)
                id_command = awk_command.id
                if id_command not in self.__num_copies_commands__.keys():
                    self.__num_copies_commands__[id_command] = 0
                self.__num_copies_commands__[id_command] += 1
                debug("Calling execute in names")
                result = self.execute()
                self.__clear_commands__()
                debug("result names",result)
                # result = subprocess.check_output(command, shell=True, executable='/bin/bash').decode()
                self.__columns__ = np.array(result.replace("\n","").split(self.__delimiter__))
                self.__columns_changed__ = False
                return self.__columns__
            else:
                return []
        else:
            return self.__columns__

#     def __names_current__(self):
#         command = "awk " + """'
#     BEGIN {
#         FS = \"""" + self.__delimiter__ + """\"
#     }
#     {
#         if (NR == 1){
#             print
#             exit
#         }
#     }
#     END {}
#     ' """
#         awk_command = Awk_command()
#         awk_command.command = command
#         awk_command.priority = 9999999999
#         awk_command.type = "names"
#         awk_command.persistance_in_time = "instance"
#         self.__commands__.append(awk_command)
#         return self

    def __to_np_arrays__(self,has_header = True):
        shape = self.shape()
        columns = np.empty(shape[1],list)
        lines = self.values(clear = False)
        lines = lines.split("\n")
        str_types = self.get_types().execute()
        types = []
        types_text = str_types.split(",")
        for type_t  in types_text:
            types.append(eval(type_t))
        line_counter = 0
        names = self.names()
        for line in lines:
            if line != "":
                command = "echo '" +line.replace("\n","") + "' | gawk -v FPAT='([^" + self.__delimiter__ + "]*)|(" + self.__string_delimiter__ + "[^" + self.__string_delimiter__ + "]+" + self.__string_delimiter__ + ")' 'BEGIN{}{for (i=1;i<=NF;i++){print($i)}}END{}' "
                result = subprocess.check_output(command, shell=True, executable='/bin/bash').decode()
                elements = result.split("\n")
                elements = elements[0:len(elements)-1]
                if line_counter == 0:
                        if has_header:
                            names = elements
                        else:
                            for i in range(len(elements)):
                                if len(elements[i]) > 0:
                                    if (elements[i][0] == "\"" and elements[i][len(elements[i])-1] == "\""):
                                        elements[i] = elements[i][1:len(elements[i])-1]
                                try:    
                                    columns[i].append(elements[i])
                                except:

                                    columns[i] = [elements[i]]

                else:
                    for i in range(len(elements)):
                        if len(elements[i]) > 0:
                            if (elements[i][0] == "\"" and elements[i][len(elements[i])-1] == "\""):
                                elements[i] = elements[i][1:len(elements[i])-1]
                        try:
                            columns[i].append(elements[i])
                        except:
                            columns[i] = [elements[i]]

                line_counter += 1
        return names,columns,types

    def to_npd(self,skip_blank_lines=False,keep_default_na=False):
#         names,columns,types = self.__to_np_arrays__()
# #         print(names)
# #         print(columns)
# #         print(types)
#         t = npd.DataFrame()
#         for i in range(len(names)):
#             try:
#                 t[names[i]] = np.array(columns[i]).astype(types[i])
#             except:
#                 try:
#                     t[names[i]] = np.array(columns[i]).astype(float)
#                 except:
#                     t[names[i]] = np.array(columns[i]).astype(str)

        # if not os.path.exists(os.path.expanduser('~') + "/.tmp/"):
        #     os.mkdir(os.path.expanduser('~') + "/.tmp/")
        # if not os.path.exists(os.path.expanduser('~') + "/.tmp/awk_dataframe/"):
        #     os.mkdir(os.path.expanduser('~') + "/.tmp/awk_dataframe/")
        #     print("Creating folder ",os.path.expanduser('~') + "/.tmp/awk_dataframe/")
        # path_output = os.path.expanduser('~') + "/.tmp/awk_dataframe/output_" + self.__id__ + ".csv"
        # self.to_csv(path_output)
        # t = npd.read_csv(path_output)
        # os.remove(path_output)

        t = npd.DataFrame()
        df = self.to_pandas(skip_blank_lines=skip_blank_lines,keep_default_na=keep_default_na)
        for name in df.columns:
            t[name] = df[name].values

        return t

    def to_pandas(self,skip_blank_lines=False,keep_default_na=False):
#         names,columns,types = self.__to_np_arrays__()
# #         print(names)
# #         print(columns)
# #         print(types)
#         df = pd.DataFrame()
#         for i in range(len(names)):
#             try:
#                 df[names[i]] = np.array(columns[i]).astype(types[i])
#             except:
#                 try:
#                     df[names[i]] = np.array(columns[i]).astype(float)
#                 except:
#                     df[names[i]] = np.array(columns[i]).astype(str)
        if not os.path.exists(os.path.expanduser('~') + "/.tmp/"):
            os.mkdir(os.path.expanduser('~') + "/.tmp/")
        if not os.path.exists(os.path.expanduser('~') + "/.tmp/awk_dataframe/"):
            os.mkdir(os.path.expanduser('~') + "/.tmp/awk_dataframe/")
            print("Creating folder ",os.path.expanduser('~') + "/.tmp/awk_dataframe/")
        path_output = os.path.expanduser('~') + "/.tmp/awk_dataframe/output_" + self.__id__ + ".csv"
        self.to_csv(path_output)
        df = pd.read_csv(path_output,skip_blank_lines=skip_blank_lines,keep_default_na=keep_default_na)
        os.remove(path_output)
        return df


    
        

    def execute(self,clear = True,to_file = False,path_sh = ""):
        keep_file = False
        if path_sh == "":
            path_sh = os.path.expanduser('~') + "/.tmp/awk_dataframe/execution_" + self.__id__ + ".sh"
        else:
            keep_file = True

        if self.__has_header__:
            has_header = 1
        else:
            has_header = 0
        output_header = has_header
        
        if len(self.__commands__) == 0:
            # if self.__nrow_original__ == 0:
            #     self.shape()
            self.__get_rows_from_to__(1,None,return_other_object=False)
            self.__commands__[0].persistance_in_time = "instance"
            self.__commands__[0].persistance_after_execution = "ephemeral"
        # for command in self.__commands__:
            # awk_command_to_file(command)

        complete_command = ""
        index = 0
        debug("length_commands ",len(self.__commands__))
        for command in self.__commands__:
            debug("level simplicity in execute",self.__level_simplicity_csv__)
            command.options["original_level_simplicity_csv"] = str(self.__level_simplicity_csv__)
            # if command != self.__commands__[len(self.__commands__)-1]:

            if command == self.__commands__[0]:
                if command.type == "to_csv":
                    if len(self.__commands__) == 1:
                        complete_command = "cp " + self.__path__ + " " + command.options["path_output"]
                    else:
                        # if self.__level_simplicity_csv__ == 0:
                        if not os.path.exists(os.path.expanduser('~') + "/.local/bin/awk_dataframe"+ "/version_" + self.__version__):
                            shutil.rmtree(os.path.expanduser('~') + "/.local/bin/awk_dataframe")
                        if not os.path.exists(os.path.expanduser('~') + "/.local/bin/awk_dataframe"+ "/parse_complex_csv.exe"):
                            if not os.path.exists(os.path.expanduser('~') + "/.local"):
                                os.mkdir(os.path.expanduser('~') + "/.local")
                            if not os.path.exists(os.path.expanduser('~') + "/.local/bin/awk_dataframe"):
                                os.mkdir(os.path.expanduser('~') + "/.local/bin/awk_dataframe")
                                path_version_file = os.path.expanduser('~') + "/.local/bin/awk_dataframe"+ "/version_" + self.__version__
                                f = open(path_version_file,"w")
                                f.close()
                            command_compile = "g++ -o " + os.path.expanduser('~') + "/.local/bin/awk_dataframe"+ "/parse_complex_csv.exe " + os.path.dirname(__file__) + "/read_file_direct_output.cpp"
                            debug("Compilation command", command_compile)
                            subprocess.check_output(command_compile, shell=True, executable='/bin/bash')
                        complete_command = "cp " + self.__path__ + " " + command.options["path_output"] + " && " +  os.path.expanduser('~') + "/.local/bin/awk_dataframe"+ "/parse_complex_csv.exe " + self.__path__
                        command.options["is_last_command"] = "0"

                else:
                    if self.__level_simplicity_csv__ == 2:
                        command.options["is_first_command"] = "0"
                        command.options["is_last_command"] = "0"
                        command.options["level_simplicity_csv"] = "2"
                        debug("Creating command",command.type,command.options)
                        awk_command_to_file(command)
                        if command.options["number_files_input"] == "1":
                            complete_command = "gawk -M -f " + command.path_execution_file + " " + self.__path__
                        else:
                            complete_command = "gawk -M -f " + command.path_execution_file + " " + command.path_temp_file + " " + self.__path__ + ""
                    elif self.__level_simplicity_csv__ == 1:
                        command.options["is_first_command"] = "1"
                        command.options["is_last_command"] = "0"
                        command.options["level_simplicity_csv"] = "1"
                        debug("Creating command",command.type,command.options)
                        awk_command_to_file(command)
                        if command.options["number_files_input"] == "1":
                            complete_command = "gawk -M -f " + command.path_execution_file + " " + self.__path__
                        else:
                            complete_command = "gawk -M -f " + command.path_execution_file + " " + command.path_temp_file + " " + self.__path__ + ""

                    else:
                        command.options["level_simplicity_csv"] = str(self.__level_simplicity_csv__)
                        command.options["is_first_command"] = "0"
                        command.options["level_simplicity_csv"] = "2"
                        if len(self.__commands__) == 1:
                            command.options["is_last_command"] = "1"
                        else:
                            # if self.__commands__[index].type in ["where","to_csv","unique"]:
                            #     command.options["is_last_command"] = "1"
                            # else:
                            command.options["is_last_command"] = "0"

                    # if command.options["is_first_command"] != command.options["is_last_command"]:
                    #     command.options["line_based_code"] = "0"

                        debug("Creating command",command.type,command.options)
                        if not os.path.exists(os.path.expanduser('~') + "/.local/bin/awk_dataframe"+ "/version_" + self.__version__):
                            shutil.rmtree(os.path.expanduser('~') + "/.local/bin/awk_dataframe")
                        if not os.path.exists(os.path.expanduser('~') + "/.local/bin/awk_dataframe"+ "/parse_complex_csv.exe"):
                                if not os.path.exists(os.path.expanduser('~') + "/.local"):
                                    os.mkdir(os.path.expanduser('~') + "/.local")
                                if not os.path.exists(os.path.expanduser('~') + "/.local/bin/awk_dataframe"):
                                    os.mkdir(os.path.expanduser('~') + "/.local/bin/awk_dataframe")    
                                    path_version_file = os.path.expanduser('~') + "/.local/bin/awk_dataframe"+ "/version_" + self.__version__
                                    f = open(path_version_file,"w")
                                    f.close()
                                command_compile = "g++ -o " + os.path.expanduser('~') + "/.local/bin/awk_dataframe"+ "/parse_complex_csv.exe " + os.path.dirname(__file__) + "/read_file_direct_output.cpp"
                                debug("Compilation command", command_compile)
                                subprocess.check_output(command_compile, shell=True, executable='/bin/bash')

                        awk_command_to_file(command)
                        if command.options["number_files_input"] == "1":
                            complete_command = "gawk -M -f " + command.path_execution_file + " <(" + os.path.expanduser('~') + "/.local/bin/awk_dataframe"+ "/parse_complex_csv.exe " + self.__path__ + ")"
                        else:
                            complete_command = "gawk -M -f " + command.path_execution_file + " " + command.path_temp_file + " <(" + os.path.expanduser('~') + "/.local/bin/awk_dataframe"+ "/parse_complex_csv.exe " + self.__path__ + ")"



                
                
            else:
                if command.type == "to_csv":
                    if not os.path.exists(os.path.expanduser('~') + "/.local/bin/awk_dataframe"+ "/version_" + self.__version__):
                        shutil.rmtree(os.path.expanduser('~') + "/.local/bin/awk_dataframe")
                    if not os.path.exists(os.path.expanduser('~') + "/.local/bin/awk_dataframe"+ "/save_csv.exe"):
                        if not os.path.exists(os.path.expanduser('~') + "/.local"):
                            os.mkdir(os.path.expanduser('~') + "/.local")
                        if not os.path.exists(os.path.expanduser('~') + "/.local/bin"):
                            os.mkdir(os.path.expanduser('~') + "/.local/bin")
                        if not os.path.exists(os.path.expanduser('~') + "/.local/bin/awk_dataframe"):
                            os.mkdir(os.path.expanduser('~') + "/.local/bin/awk_dataframe")   
                            path_version_file = os.path.expanduser('~') + "/.local/bin/awk_dataframe"+ "/version_" + self.__version__
                            f = open(path_version_file,"w")
                            f.close()
                        command_compile = "g++ -o " + os.path.expanduser('~') + "/.local/bin/awk_dataframe"+ "/save_csv.exe " + os.path.dirname(__file__) + "/write_to_file.cpp"
                        debug("Compilation command", command_compile)
                        subprocess.check_output(command_compile, shell=True, executable='/bin/bash')
                    
                           
                    
                    complete_command = os.path.expanduser('~') + "/.local/bin/awk_dataframe"+ "/save_csv.exe " + command.options["path_output"] + " <(" + complete_command + ")"             
                    
                else:

                    if self.__level_simplicity_csv__ == 2:
                        command.options["is_first_command"] = "0"
                        command.options["is_last_command"] = "0"
                        command.options["level_simplicity_csv"] = "2"
                    else:
                        command.options["level_simplicity_csv"] = str(self.__level_simplicity_csv__)
                        if self.__commands__[index - 1].options["is_last_command"] == "0":
                            command.options["is_first_command"] = "0"
                            command.options["level_simplicity_csv"] = "2"
                        else:
                            command.options["is_first_command"] = "1"
                            command.options["level_simplicity_csv"] = str(self.__level_simplicity_csv__)

                        if command == self.__commands__[len(self.__commands__)-1] and command.type not in ["shape"]:    
                            command.options["is_last_command"] = "1"
                        else:
                            # if self.__commands__[index].type in ["where","to_csv","unique"]:
                            #     command.options["is_last_command"] = "1"
                            # else:
                            command.options["is_last_command"] = "0"   

                        # if command.options["is_first_command"] != command.options["is_last_command"]:
                        #     command.options["line_based_code"] = "0"
                    if (self.__commands__[index - 1].options["is_last_command"] == "1"):
                        if int(self.__commands__[index - 1].options["level_simplicity_csv"]) > 0:
                            debug("Creating comand",command.type,command.options)
                            awk_command_to_file(command)                
                            if command.options["number_files_input"] == "1":
                                complete_command = "gawk -M -f " + command.path_execution_file + " <(" + complete_command + ")"             
                            else:
                                complete_command = "gawk -M  -f " + command.path_execution_file + " " + command.path_temp_file + " <(" + complete_command + ")"             
                        else:
                            debug("Creating command",command.type,command.options)
                            if not os.path.exists(os.path.expanduser('~') + "/.local/bin/awk_dataframe"+ "/version_" + self.__version__):
                                shutil.rmtree(os.path.expanduser('~') + "/.local/bin/awk_dataframe")
                            if not os.path.exists(os.path.expanduser('~') + "/.local/bin/awk_dataframe"+ "/parse_complex_csv.exe"):
                                if not os.path.exists(os.path.expanduser('~') + "/.local"):
                                    os.mkdir(os.path.expanduser('~') + "/.local")
                                if not os.path.exists(os.path.expanduser('~') + "/.local/bin/awk_dataframe"):
                                    os.mkdir(os.path.expanduser('~') + "/.local/bin/awk_dataframe")    
                                    path_version_file = os.path.expanduser('~') + "/.local/bin/awk_dataframe"+ "/version_" + self.__version__
                                    f = open(path_version_file,"w")
                                    f.close()
                                command_compile = "g++ -o " + os.path.expanduser('~') + "/.local/bin/awk_dataframe"+ "/parse_complex_csv.exe " + os.path.dirname(__file__) + "/read_file_direct_output.cpp"
                                debug("Compilation command", command_compile)
                                subprocess.check_output(command_compile, shell=True, executable='/bin/bash')

                            debug("Creating comand",command.type,command.options)
                            awk_command_to_file(command)                
                            if command.options["number_files_input"] == "1":
                                complete_command = "gawk -M -f " + command.path_execution_file + " <(" + os.path.expanduser('~') + "/.local/bin/awk_dataframe"+ "/parse_complex_csv.exe " + " <(" + complete_command + "))"             
                            else:
                                complete_command = "gawk -M  -f " + command.path_execution_file + " " + command.path_temp_file + " <(" + os.path.expanduser('~') + "/.local/bin/awk_dataframe"+ "/parse_complex_csv.exe " + " <(" + complete_command + "))"           
                    else:
                        debug("Creating comand",command.type,command.options)
                        awk_command_to_file(command)                
                        if command.options["number_files_input"] == "1":
                            complete_command = "gawk -M  -f " + command.path_execution_file + " <(" + complete_command + ")"             
                        else:
                            complete_command = "gawk -M -f " + command.path_execution_file + " " + command.path_temp_file + " <(" + complete_command + ")" 


                
            index += 1
            
                
        # ###################using file
        if to_file:
            if not os.path.exists(os.path.expanduser('~') + "/.tmp/"):
                os.mkdir(os.path.expanduser('~') + "/.tmp/")
            if not os.path.exists(os.path.expanduser('~') + "/.tmp/awk_dataframe/"):
                os.mkdir(os.path.expanduser('~') + "/.tmp/awk_dataframe/")
                print("Creating folder ",os.path.expanduser('~') + "/.tmp/awk_dataframe/")

            f = open(path_sh,'w')
            f.write(complete_command)
            f.close()
            result = os.popen("bash " + path_sh).read()
            if not keep_file:
                os.remove(path_sh)
        else:
            debug(complete_command)
            result = subprocess.check_output(complete_command, shell=True, executable='/bin/bash').decode()
        # ################

        new_commands = []
        for command in self.__commands__:
            if os.path.exists(command.path_execution_file):
                os.remove(command.path_execution_file)
            if command.persistance_in_time == "continuous":
                new_commands.append(command)
                debug("appending",command.type)
            else:
                self.__num_copies_commands__[command.id] -= 1
                debug("discarding",command.type)
        self.__commands__ = new_commands
        for command in self.__commands__:
            debug("active commands",command.type)
        if clear:
            self.__clear_commands__()
        return result

    def __get_rows_from_to__(self,min_row,max_row,has_header = True,output_header = True,return_other_object = True):

        awk_command = Awk_command()

        # if not self.__nrow_modified_to_unknown_value__:
        #     if min_row < 0:
        #         min_row = 0
        #     if max_row > self.__nrow__:
        #         max_row = self.__nrow__
        #     awk_command.nrow_selected = max_row-min_row
        #     awk_command.nrow_before = self.__nrow__
        #     awk_command.ncol_before = self.__ncol__
        #     self.__nrow__ = awk_command.nrow_selected

        # if self.__nrow__ > 0:
    #         if type(rows) == list:
    #             rows = np.array(rows)
    #         rows_str = np.array2string(rows,separator="\n")
    #         rows_str = rows_str[1:len(rows_str)-1]
    #         path_rows = os.path.expanduser('~') + "/.tmp/awk_dataframe/rows_" + self.__id__ + ".txt"
    #         command = "echo '" + rows_str + "'>" + path_rows
    #         os.system(command)

            # variables = "-v has_header=\"has_header_variable\" -v output_header=\"output_header_variable\" -v min_row=\"" + str(min_row) + "\" -v max_row=\"" + str(max_row) + "\" "
            # command = "gawk -v FPAT='([^" + self.__delimiter__ + "]*)|(" + self.__string_delimiter__ + "[^" + self.__string_delimiter__ + "]+" + self.__string_delimiter__ + ")' " + variables + """'
            # BEGIN {

            #     RS = "record_delimiter"
            #     RS_new = "record_delimiter_transform"



            # }
            # {
            #     if (has_header){
            #         if (FNR == 1){
            #             if (output_header){
            #                 printf("%s" RS_new,$0)
            #             }
            #         }else{
            #             if (FNR >= min_row + 2 && FNR <= max_row + 2){
            #                 printf("%s" RS_new,$0)
            #             }
            #         }

            #         if (FNR > max_row + 2){
            #             exit
            #         }
            #     }else{
            #         if (FNR >= min_row + 1 && FNR <= max_row + 1){
            #                 printf("%s" RS_new,$0)
            #         }

            #         if (FNR > max_row + 1){
            #             exit
            #         }
            #     }

            # }
            # END {

            # }
            # ' """
        awk_command.options = get_options_default()
        awk_command.options["row_start"] = str(min_row)
        if max_row is None:
            awk_command.options["row_end"] = "INF"
        else:
            awk_command.options["row_end"] = str(max_row - 1)
        awk_command.options["line_based_code"] = "1"
        awk_command.commands = get_default_commands()
        if output_header:
            awk_command.output_header = 1
        else:
            awk_command.output_header = 0
        if has_header:
            awk_command.has_header = 1
        else:
            awk_command.has_header = 0
        awk_command.priority = 1
        awk_command.type = "get_rows_range"
        self.__commands__.append(awk_command)
        id_command = awk_command.id
        if id_command not in self.__num_copies_commands__.keys():
            self.__num_copies_commands__[id_command] = 0
        self.__num_copies_commands__[id_command] += 1
        if return_other_object:
            __ddf__ = self.__deepcopy_internal__({})
            __ddf__.__settle_commands__()
            self.__clear_commands__()
            return __ddf__
        # else:
        #     raise Exception("No rows selected")

    def get_rows(self,rows,has_header = True,output_header = True,return_other_object = True):



        if type(rows) == range or type(rows) == slice:
            from_start = False
            until_end = False
            if type(rows) == slice:                
                if rows.start is None:
                    start = 0
                    from_start = True
                else:
                    start = rows.start
                if rows.stop is None:
                    # if self.__nrow_original__ == 0:
                    #     self.shape()
                    # debug("shape",self.__nrow_original__,self.__ncol_original__)
                    # stop = self.__nrow_original__
                    stop = None
                    until_end = True
                else:
                    stop = rows.stop
                if rows.step is None:
                    step = 1                    
                else:
                    step = rows.step                
                
                # rows = range(start,stop,step)
                # debug("Rows",rows)
            else:
                start = min(rows)
                stop = max(rows) + 1
            if not from_start or not until_end:
                if not until_end:
                    return DataFrame.__get_rows_from_to__(self,start + 1,stop,has_header = has_header,output_header = output_header,return_other_object = return_other_object)
                else:
                    return DataFrame.__get_rows_from_to__(self,start + 1,None,has_header = has_header,output_header = output_header,return_other_object = return_other_object)
            else:
                if return_other_object:
                    __ddf__ = self.__deepcopy_internal__({})
                    __ddf__.__settle_commands__()
                    self.__clear_commands__()
                    return __ddf__
        else:

            awk_command = Awk_command()
            if type(rows) == list:
                rows = np.array(rows)

            rows += 1

            # if not self.__nrow_modified_to_unknown_value__:
            #     rows = rows[np.where(np.isin(rows,np.arange(0,nrow)))[0]]
            #     awk_command = Awk_command()
            #     awk_command.nrow_selected = len(rows)
            #     awk_command.nrow_before = self.__nrow__
            #     awk_command.ncol_before = self.__ncol__
            #     self.__nrow__ = awk_command.nrow_selected

            rows_str = np.array2string(rows,separator="\n").replace(" ","")
            rows_str = rows_str[1:len(rows_str)-1]
            debug(rows_str)
            if not os.path.exists(os.path.expanduser('~') + "/.tmp/"):
                os.mkdir(os.path.expanduser('~') + "/.tmp/")
            if not os.path.exists(os.path.expanduser('~') + "/.tmp/awk_dataframe/"):
                os.mkdir(os.path.expanduser('~') + "/.tmp/awk_dataframe/")
                print("Creating folder ",os.path.expanduser('~') + "/.tmp/awk_dataframe/")
            path_rows = os.path.expanduser('~') + "/.tmp/awk_dataframe/rows_" + self.__id__ + "_" + awk_command.id + ".txt"
            # note("TODO: modify this to save with bash")
            # command = "echo '" + rows_str + "'>" + path_rows
            # os.system(command)

            # variables = "-v has_header=\"has_header_variable\" -v output_header=\"output_header_variable\" -v min_row=\"" + str(min(rows)) + "\" -v max_row=\"" + str(max(rows)) + "\" -v length_rows=\"" + str(len(rows)) + "\" "
            # command = "gawk -v FPAT='([^" + self.__delimiter__ + "]*)|(" + self.__string_delimiter__ + "[^" + self.__string_delimiter__ + "]+" + self.__string_delimiter__ + ")' " + variables + """'
            # BEGIN {

            #     RS = "record_delimiter"
            #     RS_new = "record_delimiter_transform"
            #     # cmd = "cat \"
            #     #
            #     # while (cmd | getline) {
            #     #     if (has_header){
            #     #         rows["1"] = 1
            #     #         rows[$0+2] = 1;
            #     #     }else{
            #     #         rows[$0+1] = 1;
            #     #     }
            #     #
            #     # }
            #     #
            #     # close(cmd)



            # }
            # {
            #     if (FNR == NR){
            #         if(has_header){
            #             rows["1"] = 1
            #             rows[$0+2] = 1

            #         }else{

            #             rows[$0+1] = 1
            #         }

            #     }else{
            #         if (has_header){
            #             if (rows[FNR] == 1){
            #                 if (FNR == 1){
            #                     if (output_header){
            #                         printf("%s" RS_new,$0)
            #                     }
            #                 }else{
            #                     printf("%s" RS_new,$0)
            #                 }
            #             }
            #             if (FNR > max_row + 2){
            #                 exit
            #             }
            #         }else{
            #             if (rows[FNR] == 1){

            #                 printf("%s" RS_new,$0)
            #                                     }
            #             if (FNR > max_row + 1){
            #                 exit
            #             }

            #         }
            #     }

            # }
            # END {

            # }
            # ' <(echo '""" + rows_str + """') """
            awk_command.options = get_options_default()
            awk_command.options["row_start"] = str(min(rows))
            awk_command.options["row_end"] = str(max(rows))
            awk_command.options["number_files_input"] = "2"
            awk_command.options["input_file_rows"] = "1"
            awk_command.options["line_based_code"] = "1"
            awk_command.commands = get_default_commands()

            to_file = False
            if to_file:
                command = "echo '" + rows_str + "'>" + path_rows
                os.system(command)
                awk_command.path_temp_file = path_rows
            else:
                awk_command.path_temp_file = """<(echo '""" + rows_str + """')"""
            if output_header:
                awk_command.output_header = 1
            else:
                awk_command.output_header = 0
            if has_header:
                awk_command.has_header = 1
            else:
                awk_command.has_header = 0
            awk_command.priority = 1
            awk_command.type = "get_rows"
            self.__commands__.append(awk_command)
            id_command = awk_command.id
            if id_command not in self.__num_copies_commands__.keys():
                self.__num_copies_commands__[id_command] = 0
            self.__num_copies_commands__[id_command] += 1
            if return_other_object:
                __ddf__ = self.__deepcopy_internal__({})
                __ddf__.__settle_commands__()
                self.__clear_commands__()
                return __ddf__


    def __get_cols_from_to__(self,min_col,max_col,has_header = True,output_header = True,return_other_object = True):
        awk_command = Awk_command()
        
        
        # awk_command.ncol_selected = max(cols) - min(cols)
        # awk_command.nrow_before = self.__nrow__
        # awk_command.ncol_before = self.__ncol__
        # self.__ncol__ = awk_command.ncol_selected

        # variables = "-v has_header=\"has_header_variable\" -v output_header=\"output_header_variable\" -v min_col=\"" + str(min(cols)) + "\" -v max_col=\"" + str(max(cols)) + "\" "
        # command = "gawk -v FPAT='([^" + self.__delimiter__ + "]*)|(" + self.__string_delimiter__ + "[^" + self.__string_delimiter__ + "]+" + self.__string_delimiter__ + ")' " + variables + """'
        # BEGIN {
        #     RS = "record_delimiter"
        #     RS_new = "record_delimiter_transform"

        # }
        # {
        #     if (has_header){
        #         if (FNR == 1){
        #             if (output_header){
        #                 for (i=min_col+1;i<max_col+1;i++){
                            
        #                     printf("%s""" + self.__delimiter__ + """", $i)
                            
        #                 }
        #                 printf("%s", $(max_col+1))
        #                 printf("%s" RS_new,"")
        #             }
        #         }else{
        #             for (i=min_col+1;i<max_col+1;i++){
                        
        #                 printf("%s""" + self.__delimiter__ + """", $i)
                        
        #             }
        #             printf("%s", $(max_col+1))
        #             printf("%s" RS_new,"")

        #         }
        #     }else{
        #         for (i=min_col+1;i<max_col+1;i++){
        #             printf("%s""" + self.__delimiter__ + """", $i)
        #         }
        #         printf("%s", $(max_col+1))
        #         printf("%s" RS_new,"")
        #     }
            

        # }
        # END {

        # }
        # ' """
        # awk_command.command = command
        awk_command.options = get_options_default()
        awk_command.options["col_start"] = str(min_col)
        if max_col is None:
            awk_command.options["col_end"] = "INF"
        else:
            awk_command.options["col_end"] = str(max_col)
        awk_command.options["number_files_input"] = "1"
        awk_command.options["input_file_rows"] = "0"
        awk_command.commands = get_default_commands()

        if output_header:
            awk_command.output_header = 1
        else:
            awk_command.output_header = 0
        if has_header:
                awk_command.has_header = 1
        else:
            awk_command.has_header = 0
        awk_command.priority = 2
        awk_command.type = "get_cols_from_to"
        self.__commands__.append(awk_command)
        id_command = awk_command.id
        if id_command not in self.__num_copies_commands__.keys():
            self.__num_copies_commands__[id_command] = 0
        self.__num_copies_commands__[id_command] += 1
        if return_other_object:
            __ddf__ = self.__deepcopy_internal__({})
            __ddf__.__settle_commands__()
            self.__clear_commands__()
            return __ddf__

    def get_cols(self,cols,has_header = True,output_header = True,return_other_object = True):
        if type(cols) == range or type(cols) == slice:            
            from_start = False
            until_end = False
            if type(cols) == slice:
                if cols.start is None:
                    start = 0
                    from_start = True
                else:
                    start = cols.start
                if cols.stop is None:
                    # if self.__ncol_original__ == 0:
                    #     self.__ncol_original__ = len(self.names())
                    # debug("length ncol",self.__ncol_original__ )
                    stop = None
                    until_end = True
                else:
                    stop = cols.stop                    
                if cols.step is None:
                    step = 1                    
                else:
                    step = cols.step                
                # cols = range(start,stop,step)
            else:
                start = min(cols)
                stop = max(cols) + 1
            if (not from_start or not until_end):
                self.__columns_changed__ = True
                if not until_end:
                    debug("get_cols__columns_changed__",self.__columns_changed__)
                    return DataFrame.__get_cols_from_to__(self,start + 1,stop,has_header = has_header,output_header = output_header,return_other_object=return_other_object)
                else:
                    return DataFrame.__get_cols_from_to__(self,start + 1,None,has_header = has_header,output_header = output_header,return_other_object=return_other_object)
            else:
                if return_other_object:
                    __ddf__ = self.__deepcopy_internal__({})
                    __ddf__.__settle_commands__()
                    self.__clear_commands__()
                    return __ddf__
        else:
            
            awk_command = Awk_command()
            if type(cols) == int or type(cols) == str:
                cols = [cols]
            if type(cols) == np.array:
                cols = cols.tolist()

            new_cols = np.empty(len(cols),int)

            names = self.names()
            self.__columns_changed__ = True
            debug("get_cols__columns_changed__",self.__columns_changed__)
            bad_cols = []
            for i in range(len(cols)):
                col = cols[i]
                if type(col) != int:

                    index = np.where(names == col)[0]                    
                    debug(type(index))
                    if len(index) == 1:
                        new_cols[i] = index[0]
                    else:
                        bad_cols.append(col)                        
                else:
                    new_cols[i] = col
            if len(bad_cols) > 0:
                raise Exception("Column name(s) not found:",bad_cols)
            cols = np.unique(new_cols)
            cols += 1
            # if not self.__nrow_modified_to_unknown_value__:
            # cols = cols[np.where(np.isin(cols,np.arange(0,self.__ncol__)))[0]]
            # col += 1
            awk_command = Awk_command()
            awk_command.ncol_selected = len(cols)
            awk_command.nrow_before = self.__nrow__
            awk_command.ncol_before = self.__ncol__
            self.__ncol__ = awk_command.ncol_selected

            cols_str = np.array2string(cols,separator="\n").replace(" ","")
            debug(cols_str)
            cols_str = cols_str[1:len(cols_str)-1]
            if not os.path.exists(os.path.expanduser('~') + "/.tmp/"):
                os.mkdir(os.path.expanduser('~') + "/.tmp/")
            if not os.path.exists(os.path.expanduser('~') + "/.tmp/awk_dataframe/"):
                os.mkdir(os.path.expanduser('~') + "/.tmp/awk_dataframe/")
                print("Creating folder ",os.path.expanduser('~') + "/.tmp/awk_dataframe/")
            path_cols = os.path.expanduser('~') + "/.tmp/awk_dataframe/cols_" + self.__id__ + "_" + awk_command.id + ".txt"
            # note("TODO: modify this to save with bash")
            # command = "echo '" + cols_str + "' | sort | xargs -I {} echo \"{}\" >" + path_cols
            # os.system(command)

            # variables = "-v has_header=\"has_header_variable\" -v output_header=\"output_header_variable\" -v min_col=\"" + str(min(cols)) + "\" -v max_col=\"" + str(max(cols)) + "\" "
            # command = "gawk -v FPAT='([^" + self.__delimiter__ + "]*)|(" + self.__string_delimiter__ + "[^" + self.__string_delimiter__ + "]+" + self.__string_delimiter__ + ")' " + variables + """'
            # BEGIN {
            #     RS = "record_delimiter"
            #     RS_new = "record_delimiter_transform"

            # }
            # {
            #     if (FNR==NR){
            #         cols[$0+1] = 1
            #     }else{
            #         if (has_header){
            #             if (FNR == 1){
            #                 if (output_header){
            #                     for (i=min_col+1;i<max_col+1;i++){
            #                         if (cols[i] == 1){
            #                             printf("%s""" + self.__delimiter__ + """", $i)
            #                         }
            #                     }
            #                     if (cols[max_col+1] == 1){
            #                         printf("%s", $(max_col+1))
            #                     }
            #                     printf("%s" RS_new,"")
            #                 }
            #             }else{
            #                 for (i=min_col+1;i<max_col+1;i++){
            #                     if (cols[i] == 1){
            #                         printf("%s""" + self.__delimiter__ + """", $i)
            #                     }
            #                 }
            #                 if (cols[max_col+1] == 1){
            #                     printf("%s", $(max_col+1))
            #                 }
            #                 printf("%s" RS_new,"")

            #             }
            #         }else{
            #             for (i=min_col+1;i<max_col+1;i++){
            #                 if (cols[i] == 1){
            #                     printf("%s""" + self.__delimiter__ + """", $i)
            #                 }
            #             }
            #             if (cols[max_col+1] == 1){
            #                 printf("%s", $(max_col+1))
            #             }
            #             printf("%s" RS_new,"")
            #         }
            #     }

            # }
            # END {

            # }
            # ' <(echo '""" + cols_str + """') """
            # awk_command.command = command
            awk_command.options = get_options_default()
            awk_command.options["col_start"] = str(min(cols))
            awk_command.options["col_end"] = str(max(cols))
            awk_command.options["number_files_input"] = "2"
            awk_command.options["input_file_rows"] = "0"
            awk_command.commands = get_default_commands()

            to_file = False
            if to_file:
                command = "echo '" + cols_str + "' | sort | xargs -I {} echo \"{}\" >" + path_cols
                os.system(command)
                awk_command.path_temp_file = path_cols
            else:
                awk_command.path_temp_file = """<(echo '""" + cols_str + """')"""

            # if output_header:
            #         awk_command.output_header = 1
            # else:
            #     awk_command.output_header = 0
            # if has_header:
            #         awk_command.has_header = 1
            # else:
            #     awk_command.has_header = 0
            awk_command.priority = 2
            awk_command.type = "get_cols"
            self.__commands__.append(awk_command)
            id_command = awk_command.id
            if id_command not in self.__num_copies_commands__.keys():
                self.__num_copies_commands__[id_command] = 0
            self.__num_copies_commands__[id_command] += 1
            if return_other_object:
                __ddf__ = self.__deepcopy_internal__({})
                __ddf__.__settle_commands__()
                self.__clear_commands__()
                return __ddf__

    def __clear_commands__(self):
        new_commands = []
        for command in self.__commands__:
            if command.persistance_after_execution != "ephemeral" and command.persistance_in_time != "instance":
                new_commands.append(command)
            else:
                self.__num_copies_commands__[command.id] -= 1
                if os.path.exists(command.path_temp_file) and self.__num_copies_commands__[command.id] <= 0:
                        # print("restore os.remove")
                    os.remove(command.path_temp_file)
                # if command.type == "get_cols":
                #     self.__ncol__ = self.__ncol_original__
                # if command.type == "get_rows":
                #     self.__nrow__ = self.__nrow_original__
                # print("num_copies ",command.num_copies)
                # if command.type == "get_cols" and self.__num_copies_commands__[command.id] <= 0:
                #     path_cols = os.path.expanduser('~') + "/.tmp/awk_dataframe/cols_" + self.__id__ + "_" + command.id + ".txt"
                #     if os.path.exists(path_cols):
                #         # print("restore os.remove")
                #         os.remove(path_cols)

                # if command.type == "get_rows" and self.__num_copies_commands__[command.id] <= 0:
                #     path_rows = os.path.expanduser('~') + "/.tmp/awk_dataframe/rows_" + self.__id__ + "_" + command.id + ".txt"
                #     if os.path.exists(path_rows):
                #         # print("restore os.remove")
                #         os.remove(path_rows)

                



        self.__commands__ = new_commands

    def __clear_all_commands__(self):
        for command in self.__commands__:
            self.__num_copies_commands__[command.id] -= 1
            if os.path.exists(command.path_temp_file) and self.__num_copies_commands__[command.id] <= 0:
                    # print("restore os.remove")
                os.remove(command.path_temp_file)
            # if command.type == "get_cols":
            #     self.__ncol__ = self.__ncol_original__
            # if command.type == "get_rows":
            #     self.__nrow__ = self.__nrow_original__
            # # print("num_copies b ",command.num_copies)
            # if command.type == "get_cols" and self.__num_copies_commands__[command.id] <= 0:
            #     path_cols = os.path.expanduser('~') + "/.tmp/awk_dataframe/cols_" + self.__id__ + "_" + command.id + ".txt"
            #     if os.path.exists(path_cols):
            #         # print("restore os.remove")
            #         os.remove(path_cols)

            # if command.type == "get_rows" and self.__num_copies_commands__[command.id] <= 0:
            #     path_rows = os.path.expanduser('~') + "/.tmp/awk_dataframe/rows_" + self.__id__ + "_" + command.id + ".txt"
            #     if os.path.exists(path_rows):
            #         # print("restore os.remove")
            #         os.remove(path_rows)


        self.__commands__ = []

    def __settle_commands__(self):
        for command in self.__commands__:
            command.persistance_after_execution = "permanent"

    # def get_types(self,n = 1000):
    #     note("TODO: missing checking for header")
    #     awk_command = Awk_command()
    #     command = "gawk -v FPAT='([^" + self.__delimiter__ + "]*)|(" + self.__string_delimiter__ + "[^" + self.__string_delimiter__ + "]+" + self.__string_delimiter__ + ")' " + """'
    #     BEGIN {

    #         number_rows = 0
    #         types[""] = "int"
    #     }
    #     {
    #         if (NR == 1){
    #             for (i=1;i<=NF;i++){
    #                 types[$i] = "int"
    #             }
    #         }else{

    #             for (i=1;i<=NF;i++){
    #                 if ($i == ""){
    #                     types[$i] = "str"
    #                 }else{
    #                     if ($i ~ /^[0-9]+$/ && types[$i] == "int"){
    #                         types[$i] = "int"
    #                     }else{
    #                         if (($i ~ /^[0-9]*[.][0-9]+$/ || $i=="Nan" || $i=="nan" || $i=="NaN" || $i=="NAN") && (types[$i] == "int" || types[$i] == "float")){
    #                             types[$i] = "float"
    #                         }else{
    #                             types[$i] = "str"
    #                         }
    #                     }
    #                 }
    #             }
    #             if (NR > """ + str(n) + """){
    #                 exit
    #             }

    #         }
    #     }
    #     END {
    #         for (i=1;i<NF;i++){
    #             printf("%s""" + self.__delimiter__ + """",types[$i])
    #         }
    #         printf("%s",types[$NF])
    #         print("")
    #     }
    #     ' """

    #     awk_command.command = command
    #     awk_command.priority = 9999999999
    #     awk_command.type = "get_cols"
    #     awk_command.persistance_in_time = "instance"
    #     self.__commands__.append(awk_command)
    #     id_command = awk_command.id
    #     if id_command not in self.__num_copies_commands__.keys():
    #         self.__num_copies_commands__[id_command] = 0
    #     self.__num_copies_commands__[id_command] += 1
    #     __ddf__ = self.__deepcopy_internal__({})
    #     __ddf__.__settle_commands__()
    #     self.__clear_commands__()
    #     return __ddf__

    def head(self,n=10):        
        self.__max_lines_print__ = n
        awk_command = Awk_command()
        # command = "gawk -v FPAT='([^" + self.__delimiter__ + "]*)|(" + self.__string_delimiter__ + "[^" + self.__string_delimiter__ + "]+" + self.__string_delimiter__ + ")' " + """'
        # BEGIN {

        # }
        # {
        #     if (NR < """ + str(n+2) + """){
        #         for (i=1;i<NF;i++){
        #             printf("%s""" + self.__delimiter__ + """",$i)
        #         }
        #         print($NF)
                
        #     }else{
        #         exit
        #     }
        # }
        # END {}
        # ' """ + self.__path__


#         awk_command.command = command
#         awk_command.priority = 9999999999
#         awk_command.type = "get_cols"
#         awk_command.persistance_in_time = "instance"
#         self.__commands__.append(awk_command)
#         __ddf__ = self.__deepcopy_internal__({})
# __ddf__.__settle_commands__()
#     self.__clear_commands__()
# return __ddf__
        # result = subprocess.check_output(command, shell=True, executable='/bin/bash').decode()



        # awk_command.options = get_options_default()
        # awk_command.options["row_start"] = str(1)
        # awk_command.options["row_end"] = str(11)
        # awk_command.commands = get_default_commands()
        # awk_command_to_file(awk_command)
        # command = "gawk -f " + awk_command.path_execution_file + " " + self.__path__
        # result = subprocess.check_output(command, shell=True, executable='/bin/bash').decode()
        return self.__head_current__(n = n)

    def __head_current__(self,n=10):
        awk_command = Awk_command()
        # command = "gawk -v FPAT='([^" + self.__delimiter__ + "]*)|(" + self.__string_delimiter__ + "[^" + self.__string_delimiter__ + "]+" + self.__string_delimiter__ + ")' " + """'
        # BEGIN {

        # }
        # {
        #     if (NR < """ + str(n+2) + """){
        #         for (i=1;i<NF;i++){
        #             printf("%s""" + self.__delimiter__ + """",$i)
        #         }
        #         print($NF)
                
        #     }else{
        #         exit
        #     }
        # }
        # END {}
        # ' """


        # awk_command.command = command
        awk_command.options = get_options_default()
        awk_command.options["row_start"] = str(0)
        awk_command.options["row_end"] = str(n+1)
        awk_command.commands = get_default_commands()
        awk_command.priority = 9999999999
        awk_command.type = "head"
        awk_command.persistance_in_time = "instance"
        self.__commands__.append(awk_command)
        id_command = awk_command.id
        if id_command not in self.__num_copies_commands__.keys():
            self.__num_copies_commands__[id_command] = 0
        self.__num_copies_commands__[id_command] += 1
        return self

    def where(self,condition,has_header = True,output_header = True,verbose = True):
        if type(condition) == str:
            conditional_equation = Conditional_equation()
            conditional_equation.__columns__ = self.names()
            conditional_equation.condition = condition
            conditional_equation.__verbose__ = verbose
        elif (type(condition) == Conditional_equation):
            conditional_equation = Conditional_equation()
            conditional_equation.__columns__ = self.names()
            conditional_equation.equation = condition.equation
            conditional_equation.condition = condition.condition
            conditional_equation.__verbose__ = verbose

        self.__nrow_modified_to_unknown_value__ = True


#         print(condition)
        # command = """gawk -v FPAT='([^""" + self.__delimiter__ + "]*)|(" + self.__string_delimiter__ + "[^" + self.__string_delimiter__ + "]+" + self.__string_delimiter__ + """)' '
        # BEGIN {

        #     column = column+1
        # }
        # {
        #     if (NR == 1){
        #         print $0
        #     }else{                
        #         if (""" + conditional_equation.condition + """){
        #             print $0
        #         }else{

        #         }

        #     }
        # }
        # END {}
        # ' """

    

#         print(command)
        awk_command = Awk_command()
        awk_command.options = get_options_default()
        awk_command.options["line_based_code"] = "0"
        awk_command.commands = get_default_commands()

        debug(conditional_equation.condition)
        awk_command.commands["command_condition"] = conditional_equation.condition
        # awk_command.command = command
        awk_command.priority = 1
        awk_command.type = "where"
        self.__commands__.append(awk_command)
        id_command = awk_command.id
        if id_command not in self.__num_copies_commands__.keys():
            self.__num_copies_commands__[id_command] = 0
        self.__num_copies_commands__[id_command] += 1
        __ddf__ = self.__deepcopy_internal__({})
        __ddf__.__settle_commands__()
        self.__clear_commands__()
        return __ddf__

    def modify(self,equation):
        if type(equation) == str:
            note("TODO: allow to use | to determine condition and ; to separate equations")
            conditional_equation = Conditional_equation()
            conditional_equation.__columns__ = self.names()
            conditional_equation.equation = equation
        elif type(equation) == Conditional_equation:
            conditional_equation = Conditional_equation()
            conditional_equation.__columns__ = self.names()
            conditional_equation.equation = equation.equation
            conditional_equation.condition = equation.condition

        awk_command = Awk_command()
        awk_command.options = get_options_default()
        awk_command.options["line_based_code"] = "0"
        awk_command.commands = get_default_commands()

        debug(conditional_equation.equation)        
        awk_command.commands["commands_transform_column"] = conditional_equation.equation
        # awk_command.command = command
        awk_command.priority = 1
        awk_command.type = "modify"
        self.__commands__.append(awk_command)
        id_command = awk_command.id
        if id_command not in self.__num_copies_commands__.keys():
            self.__num_copies_commands__[id_command] = 0
        self.__num_copies_commands__[id_command] += 1
        __ddf__ = self.__deepcopy_internal__({})
        __ddf__.__settle_commands__()
        self.__clear_commands__()
        return __ddf__

    def add_column(self,name_column):
        self.__columns_changed__ = True
        awk_command = Awk_command()
        awk_command.options = get_options_default()
        awk_command.options["name_new_column"] = name_column
        awk_command.options["add_new_column"] = "1"
        awk_command.options["line_based_code"] = "0"
        awk_command.commands = get_default_commands()
        # awk_command.command = command
        awk_command.priority = 1
        awk_command.type = "add_column"
        self.__commands__.append(awk_command)
        id_command = awk_command.id
        if id_command not in self.__num_copies_commands__.keys():
            self.__num_copies_commands__[id_command] = 0
        self.__num_copies_commands__[id_command] += 1
        __ddf__ = self.__deepcopy_internal__({})
        __ddf__.__settle_commands__()
        self.__clear_commands__()
        return __ddf__


    def to_csv(self,path_output,append=False,__clear_all_commands__ = False,set_as_new_path = False,remove_escape_quotes=False,remove_all_quotes = False):
        if not append:
            # if len(self.__commands__) == 0:
            #     self.get_rows(range(self.__nrow_original__),return_other_object=False)
            #     self.__commands__[0].persistance_in_time = "instance"
            #     self.__commands__[0].persistance_after_execution = "ephemeral"

            # if remove_escape_quotes:
            #     command = "gawk '{gsub(/^\"|\",|,\"|\"$/,\"\");print $0 >\"" + path_output + "\"}' "
            # elif remove_all_quotes:
            #     command = "gawk '{gsub(/\"/,\"\");print $0 >\"" + path_output + "\"}' "
            # else:
            #     command = "gawk '{print $0 >\"" + path_output + "\"}' "


            awk_command = Awk_command()
            awk_command.options = get_options_default()
            awk_command.options["save"] = "1"
            awk_command.options["path_output"] = path_output
            # awk_command.options["line_based_code"] = "0"
            awk_command.commands = get_default_commands()
            # awk_command.command = command
            awk_command.priority = 999999999999
            awk_command.type = "to_csv"
            awk_command.persistance_in_time = "instance"
            self.__commands__.append(awk_command)
            id_command = awk_command.id
            if id_command not in self.__num_copies_commands__.keys():
                self.__num_copies_commands__[id_command] = 0
            self.__num_copies_commands__[id_command] += 1
            self.execute()

            if set_as_new_path:
                self.__path__ = path_output
            if __clear_all_commands__:
                self.__clear_all_commands__()
        else:
            print("not yet implemented")
            # if remove_escape_quotes:
            #     command = "gawk '{gsub(/^\"|\",|,\"|\"$/,\"\");print $0 >>\"" + path_output + "\"}' "
            # elif remove_all_quotes:
            #     command = "gawk '{gsub(/\"/,\"\");print $0 >>\"" + path_output + "\"}' "
            # else:
            #     command = "gawk '{print $0 >>\"" + path_output + "\"}' "
            # awk_command = Awk_command()
            # awk_command.command = command
            # awk_command.priority = 999999999999
            # awk_command.type = "to_csv"
            # awk_command.persistance_in_time = "instance"
            # self.__commands__.append(awk_command)
            # id_command = awk_command.id
            # if id_command not in self.__num_copies_commands__.keys():
            #     self.__num_copies_commands__[id_command] = 0
            # self.__num_copies_commands__[id_command] += 1
            # self.execute()
            # if set_as_new_path:
            #     self.__path__ = path_output
            # if __clear_all_commands__:
            #     self.__clear_all_commands__()

    def sort_by_column(self,column,parallel = True,num_cores = 4,output_header = True,has_header = True,return_other_object = True):
        # function_bash = """body() {
        #         IFS= read -r header
        #         printf '%s\n' "$header"
        #         "$@"
        #     }"""
        # result = subprocess.check_output(function_bash, shell=True, executable='/bin/bash').decode()

        substitution_delimiter = ","

        if type(column) == int:
            column += 1
        elif type(column) == str:            
            column = np.where(self.names() == column)[0][0] + 1
            
        # command_1 = """gawk -vFPAT='([^""" + self.__delimiter__ + """]*)|(""" + self.__string_delimiter__ + """[^""" + self.__string_delimiter__ + """]+""" + self.__string_delimiter__ + """)' '
        # {
        # for (i=1;i<NF;i++){
        #     gsub(\"""" + substitution_delimiter + """","_#_",$i)
        #     printf("%s""" + substitution_delimiter + """",$i)
        # }
        # gsub(\"""" + substitution_delimiter + """","_#_",$NF)
        # print($NF)
        
        # }' """
        awk_command = Awk_command()
        # awk_command.command = command_1
        awk_command.options = get_options_default()    
        # awk_command.options["is_last_command"] = "0"
        awk_command.commands = get_default_commands()
        if output_header:
            awk_command.output_header = 1
        else:
            awk_command.output_header = 0
        if has_header:
            awk_command.has_header = 1
        else:
            awk_command.has_header = 0
        awk_command.priority = 1
        awk_command.type = "prepare_sort"
        self.__commands__.append(awk_command)
        id_command = awk_command.id
        if id_command not in self.__num_copies_commands__.keys():
            self.__num_copies_commands__[id_command] = 0
        self.__num_copies_commands__[id_command] += 1

        
        # command_2 = """gawk 'NR==1{print $0;next}{print $0| "sort -t'""" + substitution_delimiter + """' --parallel """ + str(num_cores) + """ -nk""" + str(column) + """"}' """
        awk_command = Awk_command()
        # awk_command.command = command_2
        awk_command.options = get_options_default()
        awk_command.options["sort"] = "1"
        awk_command.options["sort_column"] = str(column)
        awk_command.options["line_based_code"] = "1"
        # awk_command.options["is_last_command"] = "0"
        # awk_command.options["is_first_command"] = "0"
        awk_command.commands = get_default_commands()
        # if output_header:
        #     awk_command.output_header = 1
        # else:
        #     awk_command.output_header = 0
        # if has_header:
        #     awk_command.has_header = 1
        # else:
        #     awk_command.has_header = 0
        awk_command.priority = 1
        awk_command.type = "sort"
        self.__commands__.append(awk_command)
        id_command = awk_command.id
        if id_command not in self.__num_copies_commands__.keys():
            self.__num_copies_commands__[id_command] = 0
        self.__num_copies_commands__[id_command] += 1

        # command_3 = """gawk -vFPAT='([^""" + substitution_delimiter + """]*)|(""" + self.__string_delimiter__ + """[^""" + self.__string_delimiter__ + """]+""" + self.__string_delimiter__ + """)' '
        # {
        # for (i=1;i<NF;i++){
        #     gsub("_#_",\"""" + substitution_delimiter + """",$i)
        #     printf("%s""" + self.__delimiter__ + """",$i)

        # }
        # gsub("_#_",\"""" + substitution_delimiter + """",$NF)
        # print($NF)
        # }' """

        awk_command = Awk_command()
        # awk_command.command = command_3
        awk_command.options = get_options_default()    
        # awk_command.options["is_first_command"] = "0"
        # awk_command.options["is_last_command"] = "1"
        awk_command.commands = get_default_commands()
        # if output_header:
        #     awk_command.output_header = 1
        # else:
        #     awk_command.output_header = 0
        # if has_header:
        #     awk_command.has_header = 1
        # else:
        #     awk_command.has_header = 0
        awk_command.priority = 1
        awk_command.type = "recompose_after_sort"
        self.__commands__.append(awk_command)
        id_command = awk_command.id
        if id_command not in self.__num_copies_commands__.keys():
            self.__num_copies_commands__[id_command] = 0
        self.__num_copies_commands__[id_command] += 1
        if return_other_object:
            __ddf__ = self.__deepcopy_internal__({})
            __ddf__.__settle_commands__()
            self.__clear_commands__()
            return __ddf__
    
    def unique(self,column,output_header = True,has_header = True,return_other_object = True):
        debug("before calling names in unique")
        if type(column) == int:
            column += 1
        elif type(column) == str:            
            column = np.where(self.names() == column)[0][0] + 1
        debug("after calling names in unique")

        # command_3 = """gawk -vFPAT='([^""" + self.__delimiter__ + """]*)|(""" + self.__string_delimiter__ + """[^""" + self.__string_delimiter__ + """]+""" + self.__string_delimiter__ + """)' '
        # BEGIN{

        # }
        # !buildRec() { next }
        # {
        #     if (NR == 1){
        #         print($""" + str(column) + """)
        #     }
        #     if (NR > 1){
        #         unique[$""" + str(column) + """] = 1
        #     }
        # }
        # END{
        #     for (key in unique){
        #         print(key)
        #     }
        # }' """

        awk_command = Awk_command()
        # awk_command.command = command_3
        awk_command = Awk_command()
        awk_command.options = get_options_default()
        awk_command.options["find_unique"] = "1"
        awk_command.options["print_fields"] = "0"
        awk_command.options["col_start"] = str(column)
        awk_command.options["col_end"] = str(column)
        awk_command.commands = get_default_commands()
        # if output_header:
        #     awk_command.output_header = 1
        # else:
        #     awk_command.output_header = 0
        # if has_header:
        #     awk_command.has_header = 1
        # else:
        #     awk_command.has_header = 0
        awk_command.priority = 1
        awk_command.type = "unique"
        self.__commands__.append(awk_command)
        id_command = awk_command.id
        if id_command not in self.__num_copies_commands__.keys():
            self.__num_copies_commands__[id_command] = 0
        self.__num_copies_commands__[id_command] += 1        

        if return_other_object:
            __ddf__ = self.__deepcopy_internal__({})
            __ddf__.__settle_commands__()
            self.__clear_commands__()
            return __ddf__
        
        
        



def read_csv(path,delimiter = ",",has_header = True,names_columns = [],string_delimiter = "\"",fields_may_contain_delimiter = True,fields_may_contain_line_breaks = True):
    __ddf__ = DataFrame()
    __ddf__.read_csv(path,delimiter = delimiter,has_header = has_header,names_columns = names_columns,string_delimiter = string_delimiter,fields_may_contain_delimiter = fields_may_contain_delimiter,fields_may_contain_line_breaks = fields_may_contain_line_breaks)
    return __ddf__

