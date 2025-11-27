from django.shortcuts import render,redirect
from django.db import connection
from django.core.files import File
from .forms import UploadFileForm
import csv
import pandas as pd
import json






def showtables(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name NOT LIKE 'django%'
            AND table_name NOT LIKE 'auth%'
            AND table_name NOT LIKE 'accounts%';
        """)
        tables = cursor.fetchall()
        print(tables)
        list_tables=[]
        for i in tables:
            list_tables.append(i[0])
            
    return render(request, 'showtables.html', {"list_tables": list_tables})



def values_get(request,table_name):
    with connection.cursor() as cursor:
        cursor.execute(f"""
            select * from {table_name};"""
        )
        table_details=cursor.fetchall()
        print(table_details)
        print("th",cursor.description)
        th=[]
        data=[]
        for i in cursor.description:
            th.append(i[0])
        for i in table_details:
            data.append(i)
        print('data',data) 
        print(th)
        table_id=[]
        for i in data:
            table_id.append(i[0])
        print(table_id)          
        return render(request,'tabledetails.html',{"data":data,"table_name":table_name,"th":th,"table_id":table_id})
    return render(request,'showtables.html')

def tabledetails(request):
    return render(request,'tabledetails.html')


def dynamic_table(request):
    if request.method=="POST":
        print(request.POST)
        table_name_get=request.POST.get('table_name')
        table_name_lower=table_name_get.lower()
        table_name=table_name_lower.replace(" ","_")

        # table_name= request.POST.get('table_name')
        # name=request.POST.get('name')
        # age=request.POST.get('age')
        # address=request.POST.get('address')
        label=request.POST.getlist('Label')
        datatype=request.POST.getlist('datatype')
        Mandatory=request.POST.getlist('Mandatory')
        options=request.POST.getlist('options')

        update=",".join(label)
        lower=update.lower()
        label_field=lower.replace(' ','_')
        # sp_label=label.split(",")
        print('label_field',label_field)
        print(type(label_field))
        sp=label_field.split(",")
        final_label=list(sp)
        print('final_list',final_label)
        # print("lst_field",lst_field)

        print('update',update)
        print('lower',lower)
        print('table_name',table_name)
        print('label',label)
        print('datatype',datatype)
        print('Mandatory',Mandatory)
        print('options',options)
        lab=[]
        sep=list(zip(final_label,datatype,Mandatory,options))
        for i in sep:
            if i=="":
                continue
            else:
                lab.append(" ".join(i))
        field_create=",".join(lab)
        print("field_create",field_create)
        
        with connection.cursor() as cursor:
            cursor.execute(
                f"CREATE TABLE {table_name}({table_name}_id SERIAL PRIMARY KEY,{field_create});"
            )
            return redirect(f'/insert_values/{table_name}/')
    return render(request,"create_table.html")


def dynamic_insert(request,table_name):
    with connection.cursor() as cursor:
            cursor.execute(f"""
                select * from {table_name};"""
            )
            table_details=cursor.fetchall()
            print(cursor.description)
            table_fields=[]
            for i in cursor.description:
                if i[0]==f"{table_name}_id":
                    continue
                else:
                    table_fields.append(i[0])
            if request.method=="POST":
                print(request.POST)
                print("table_name",table_name)
                print("title",request.POST.get('title'))

                keys=[]
                values=[]
                for key,value in request.POST.items():
                    if key=="csrfmiddlewaretoken":
                        continue
                    else:
                        keys.append(key)
                        values.append(value)
                print(keys)
                print(values)
                field=",".join(keys)
                val=",".join(["%s"] * len(values))
                print("field",field)
                print("values",val)
                print('lst',values)

                # final=",".join(values)
                # print('field',field)
                # print('final',final)
                # with connection.cursor() as cursor:
                #     cursor.execute(
                #         f"""INSERT INTO {table_name} ({field}) VALUES ({final})""",
                #         values
                #     )
                #     return redirect(f"/insert_values/{table_name}/")

                with connection.cursor() as cursor:
                    cursor.execute(
                        f"INSERT INTO {table_name} ({field}) VALUES ({val})",
                        values
                    )
                    return redirect(f"/insert_values/{table_name}/")
                
    return render(request, 'insert.html',{'table_fields':table_fields,"table_details":table_details})

def drop_table(request,table_name):
    with connection.cursor() as cursor:
        cursor.execute(
                f"DROP TABLE {table_name}"
        )
        return redirect('showtables')
    return render(request,'showtables.html')

def view_fields(request,table_name):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = '{table_name}';
        """)
        fields=cursor.fetchall()
        print('fields',fields)
        print('des',cursor.description),
        
        label=[]
        types=[]
        for i in fields:
            label.append(i[0])
            types.append(i[1])
        return render(request,'view_fields.html',{'fields':fields,"table_name":table_name,"label":label,"types":types})
    return render(request,'showtable.html')

def values_delete(request, table_name, id):
    with connection.cursor() as cursor:
        cursor.execute(f"DELETE FROM {table_name} WHERE {table_name}_id = {id}")
    return redirect('values_get', table_name=table_name)


def values_update(request,table_name,id):
    
    with connection.cursor() as cursor:
        cursor.execute(f'select * from {table_name} WHERE {table_name}_id={id}')
        
        fields=cursor.fetchall()
        print(fields)
        table_fields=[]
        for i in cursor.description:
            if i[0]==f"{table_name}_id":
                continue
            else:
                table_fields.append(i[0])
        print('des',cursor.description)
        if request.method=="POST":
            keys=[]
            values=[]
            for key,value in request.POST.items():
                print('keys',key)
                print('values',value)
                if key == "csrfmiddlewaretoken":
                    continue
                else:
                    keys.append(key)
                    values.append(value)
                    
            print('final_keys',keys)
            print('final_values',values)

            pair=list(zip(keys,values))
            print('pair',pair)

            lst=[]
            for i in pair:
                lst.append("=".join(i))
            print('lst',lst)

            final=",".join(lst)
            print('final',final)
            print('inside',f"UPDATE {table_name} SET {final} WHERE {table_name}_id={id};")
            last=final.replace("=","='")
            print(last)
            final_field=last.replace(",","',")
            print("final_field",final_field)
            print('last',f"UPDATE {table_name} SET {final_field}' WHERE {table_name}_id={id};")

            cursor.execute(f"UPDATE {table_name} SET {final_field}' WHERE {table_name}_id={id};")
            return redirect('values_get', table_name=table_name)
    return render(request,'updaterow.html',{'fields':fields,"table_fields":table_fields})


from django.shortcuts import render
           
def upload_file(request,table_name):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        print('form',form)
        file_name=request.FILES['file']
        print('file_name',file_name)
        if form.is_valid():
            # data = pd.read_csv(file_name)
            # print(data)
            df = pd.read_csv(file_name)
            # headers=list(df.columns)
            # print('headers:',headers)
            # rows_only=df.values.tolist()
            # print('rows_only',rows_only)
            df.to_json('output.json', orient='records')
            with connection.cursor() as cursor:
                    cursor.execute(f'select * from {table_name} limit0;')
                    db_col=[]
                    for i in cursor.description:
                        print('i[0]',i[0])
                        if i[0]==f'{table_name}_id':
                            continue
                        else:
                            db_col.append(i[0])
                    print('db_col',db_col)
            
            with open('output.json', 'r') as file:
                data = json.load(file)
                print('data[0]',data[0])
                headers=list(data[0].keys())
                print(headers)

                head=[]
                for i in headers:
                    val=''.join(i.lower()).replace(' ','_')
                    if val in db_col:
                        head.append(i)
                print('head',head)

                val=[]
                for i in data:
                    val.append([i.get(key_value) for key_value in head])
                print(val)

                col=",".join(head)
                columns=col.lower().replace(" ","_")
                print('columns',columns)


                string=''
                for i in val:
                    string+=str(tuple(i))+','
                print(string)

                values=string.rstrip(',')
                print('columns',columns)
                print('values',values)

                
                with connection.cursor() as cursor:
                    cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES{values};")
                    return redirect('showtables')
            
                return redirect('upload_file', table_name=table_name)
    else:
        form = UploadFileForm()
    return render(request, "upload.html", {"form": form})
