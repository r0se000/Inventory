from django.shortcuts import render, redirect
from .models import Input, Output, Product
from django.db import connection

# cursor
def exe(x):     
    cursor=connection.cursor()
    cursor.execute(x)
    result=cursor.fetchall()
    return result
# -----------------------------------------------------------------------------------
#압고페이지(input.html)에서 입고내역들 보여줌
def input(request):
    query = """
    select p_name, product.device_id, input_date, price 
    from product, input 
    where product.device_id = input.device_id order by input_date desc"""
    datas=exe(query)
    contents = list()
    for i in datas:
        d=dict()
        d['p_name'] = i[0]
        d['device_id'] = i[1]
        d['input_date'] = i[2]
        d['price'] = i[3]
        contents.append(d)
    return render(request, 'input.html', {'contents':contents})
#입고된 내역 받아옴.
def input_add(request):
    product = Product()
    input = Input()
    
    product.p_name = request.GET['pname']
    product.device_id = request.GET['device_id']
    input.device_id =product.device_id
    input.input_date=request.GET['input_date']
    input.price=request.GET['price']
    product.save()
    input.save()

    return redirect('input')
# -----------------------------------------------------------------------------------
#출고페이지(output.html)에서 출고내역 보여줌
def output(request):
    query = """
    select p_name, product.device_id, output_date, cus_name 
    from product, output
    where product.device_id = output.device_id order by output_date desc"""
    datas=exe(query)

    contents = list()
    for i in datas:
        d=dict()
        d['p_name'] = i[0]
        d['device_id'] = i[1]
        d['output_date'] = i[2]
        d['cus_name'] = i[3]
        contents.append(d)
    return render(request, 'output.html', {'contents':contents})
#출고된 내역 받아옴.
def output_add(request):
    output = Output()
    output.device_id = request.GET['device_id']
    output.cus_name=request.GET['cus_name']
    output.output_date=request.GET['output_date']
    output.save()

    return redirect('output')
# -----------------------------------------------------------------------------------
# 기기별 남은 수량 조회 함수(B->BCG, C->CCTV)

def Bstored():      
    BCG="""
    select count(product.device_id) as cnt 
    from product, input 
    where p_name="BCG"&& product.device_id=input.device_id 
    union all select count(product.device_id) as cnt 
    from product, output 
    where p_name="BCG"&& product.device_id=output.device_id"""

    b=exe(BCG)

    result= b[0][0]-b[1][0]    
    return result

def Cstored():      
    CCTV="""
    select count(product.device_id) as cnt 
    from product, input 
    where p_name="CCTV"&& product.device_id=input.device_id 
    union all select count(product.device_id) as cnt 
    from product, output 
    where p_name="CCTV"&& product.device_id=output.device_id"""

    c=exe(CCTV)
    result= c[0][0]-c[1][0]    
    return result

def search(request):
    return render(request, 'search.html')

def psearch_result(request):
    con=request.GET['con']
    query="""
        select p_name, {}_date, count(*) 
        from product, {} 
        where product.device_id={}.device_id 
        group by p_name, {}_date 
        order by p_name, {}_date asc"""

    elsequery="""
        select p_name, {}_date, count(*) 
        from product, {} 
        where product.device_id={}.device_id && product.p_name='{}'
        group by p_name, {}_date 
        order by p_name, {}_date asc"""

    if con=='ALL':
        idatas=exe(query.format('input','input','input','input','input'))
        odatas=exe(query.format('output','output','output','output','output'))

        icontents = list()
        for data in idatas:
            i=dict()
            i['p_name']=data[0]
            i['input_date']=data[1]
            i['count']=data[2]
            icontents.append(i)

        ocontents = list()
        for data in odatas:
            o=dict()
            o['p_name']=data[0]
            o['output_date']=data[1]
            o['count']=data[2]
            ocontents.append(o) 
        
        bcounts=Bstored()
        ccounts=Cstored()
        return render(request, 'search.html', {'icontents':icontents, 'ocontents':ocontents, 'bcounts': bcounts, 'ccounts':ccounts, 'con':con})

    elif con=='BCG':
        idatas=exe(elsequery.format('input','input','input','BCG','input','input'))
        odatas=exe(elsequery.format('output','output','output','BCG','output','output'))

        icontents = list()
        for data in idatas:
            i=dict()
            i['p_name']=data[0]
            i['input_date']=data[1]
            i['count']=data[2]
            icontents.append(i)

        ocontents = list()
        for data in odatas:
            o=dict()
            o['p_name']=data[0]
            o['output_date']=data[1]
            o['count']=data[2]
            ocontents.append(o) 
        
        bcounts=Bstored()
        return render(request, 'search.html', {'icontents':icontents, 'ocontents':ocontents, 'bcounts': bcounts, 'con':con})

    else:
        idatas=exe(elsequery.format('input','input','input','CCTV','input','input'))
        odatas=exe(elsequery.format('output','output','output','CCTV','output','output'))

        icontents = list()
        for data in idatas:
            i=dict()
            i['p_name']=data[0]
            i['input_date']=data[1]
            i['count']=data[2]
            icontents.append(i)

        ocontents = list()
        for data in odatas:
            o=dict()
            o['p_name']=data[0]
            o['output_date']=data[1]
            o['count']=data[2]
            ocontents.append(o) 
        
        ccounts=Cstored()
        return render(request, 'search.html', {'icontents':icontents, 'ocontents':ocontents, 'ccounts':ccounts, 'con':con})

# ============================================================================================================================================
#기간별 입출고내역 조회
def search_date(request):
    return render(request, 'search_date.html')

def dsearch_result(request):

    start=request.GET['startdate']
    end=request.GET['enddate']
    p_name=request.GET['con']
    base=request.GET['basedate']

    query="""
        select p_name, product.device_id, input_date, output_date, cus_name 
        from product 
        right join input on product.device_id=input.device_id 
        left join output on input.device_id=output.device_id 
        where date({}.{}_date) between '{}' and '{}' order by {}_date desc;"""
            
    elsequery="""
        select p_name, product.device_id, input_date, output_date, cus_name 
        from product 
        right join input on product.device_id=input.device_id 
        left join output on input.device_id=output.device_id 
        where p_name='{}' &&  date({}.{}_date) between '{}' and '{}' order by {}_date desc;"""

    if p_name=='ALL':
        if base=='inputdate':
            datas=exe(query.format('input','input', start, end,'input'))
        else:
            datas=exe(query.format('output','output', start, end,'output'))
    else:
        if base=='inputdate':
            datas=exe(elsequery.format(p_name, 'input','input', start, end,'input'))
        else:
            datas=exe(elsequery.format(p_name, 'output','output', start, end,'output'))

    # datas=exe(usequery)
    contents = list()
    for i in datas:
        d=dict()
        d['p_name'] = i[0]
        d['device_id'] = i[1]
        d['input_date'] = i[2]
        d['output_date'] = i[3]
        d['cus_name'] = i[4]
        contents.append(d)

    return render(request, 'search_date.html', {'contents':contents})

# ============================================================================================================================================
#정보삭제

def delete(request):
    return render(request, 'delete.html')

def delete_result(request):
    p_name=request.GET['pname']
    device_id=request.GET['device_id']

    query="""
    delete from {} where device_id='{}';"""
    odelete=exe(query.format('output',device_id))
    idelete=exe(query.format('input',device_id))
    pdelete=exe(query.format('product',device_id))

    return render(request, 'delete_ok.html', {'p_name':p_name, 'device_id':device_id})

def delete_ok(request):
    return render(request, 'delete_ok.html')
    