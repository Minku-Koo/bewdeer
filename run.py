# 2019 09 11 Beaudeer Project Start. made by Koo Minku
# IP Address :  203.252.231.52
# Linux Address : 203.252.237.149

from flask import Flask, redirect, url_for, request, render_template
import pymysql
import json, os, re
from datetime import date, datetime, timedelta
from flask import session,  jsonify
from werkzeug import secure_filename
import operator
#from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.secret_key = 'S0sA1lykaanWa11_sL^eK$n-450w'

#이미지 첨부 시, 이미지 파일 형식인지 검사 함수
def ImgFileCheck(img_list):
    img_extensions = ['ai', 'jpg', 'jpeg',  'raw', 'png', 'psd', ]
    
    if img_list == '?':
        return 100
    
    list = img_list.split('?').remove('')
    #list.remove('')
    for name in list:
        chk = 0
        extension = name.split('.')[-1]
        
        for e in img_extensions:
            if e == extension.lower():
                chk = 1
                break
                
        if chk != 1:
            return 0
        
    return 100

"""
user 정보 database table
create table user(
     no bigint(10) unsigned NOT NULL auto_increment,
     id_value varchar(30) not null,
     name varchar(30) ,
     password varchar(30),
     email varchar(60),
     signup_date datetime,
     primary key(no));
*************************************************
게시글 정보 database table
create table post(
     no bigint(10) unsigned NOT NULL auto_increment,
     id_value varchar(30) not null,
     name varchar(30) ,
     title varchar(30),
     deadline datetime,
     cost bigint(8),
     hurry varchar(5),
     category varchar(25),
     content varchar(10000),
     upload_date datetime,
     img varchar(40),
     star bigint(4),
     `show` char(10),
     dat_count int(5),
     primary key(no) );
*************************************************
댓글답글 정보 database table
create table comment<post_no>(
    no bigint(10) unsigned NOT NULL auto_increment,
    id_value varchar(30) not null,
    name varchar(30) ,
    comment varchar(250),
    star varchar(5),
    org_comment varchar(5),
    date datetime,
    primary key(no));
"""
# 로그인 되어있으면 아이디 정보를 할당
def LogOnOff():
    if 'id' in session:
        return session.get('id')
    return ''

# 마감날짜 계산 함수
def CountDeadline(now, dead):
    now_y = int(now[:4])
    now_m = int(now[5:7])
    now_d = int(now[8:10])
    
    dead_y = int(dead[:4])
    dead_m = int(dead[5:7])
    dead_d = int(dead[8:10])
    
    # daedline - now_day
    day = date(dead_y, dead_m,dead_d) - date(now_y,now_m,now_d)
    day = str(day).split(' ')[0]
    
    if day == "0:00:00" or int(day) < 0:
        day = 'over'
    
    return day
    
#시간 계산
def CountTime(uploadtime):
    nowtime = datetime.now() - timedelta(hours=5)
    result = str(uploadtime-nowtime).split(',')
    #시간으로만 계산가능
    if len(result) == 1:
        #몇시간 전까지 할 것인가?? nowtime 값과 아랫 값 동시 변경
        if int(result[0][0])<6:
            return result[0][0]
        else:
            return 0
    #날짜 계산이 가능할때
    #else:
    return 0


#데이터베이스 연결 정보
def db_connect():
    db = pymysql.connect( host='localhost',
                          port = 3306,
                          user='root',
                          passwd='rnalsrn12',
                          db='bde_server'
                         )
    return db
    
#테이블에 원하는 값이 존재하는가
def exist_table(table, field, input):
    db=db_connect()
    #DB를 열어서 아이디가 있는지 판단
    cursor = db.cursor()
    cursor.execute( "SELECT EXISTS ( SELECT * FROM %s WHERE  '%s'='%s') as success" %(table, field, input))    
    result = cursor.fetchone()[0]
    cursor.close()
    db.close()
    return result
    
# 메인 페이지
@app.route('/')
def bde_world():
    return render_template('index.html', id=LogOnOff())
    
# 현재 날짜 알려줌
def TimeNow():
    cursor = db_connect().cursor()
    date = cursor.execute( "SELECT now()")
    date = cursor.fetchone()[0]
    cursor.close()
    
    return date

#이름 반환
def WhatYourName(id):            
    cursor = db_connect().cursor()
    cursor.execute( "SELECT name from user where id_value='%s'" %id)
    name = cursor.fetchone()[0]
    cursor.close()
    
    return name

# 로그인 페이지
@app.route('/LoginPage')
def LoginPage():
    if 'id' in session:
        return render_template('myprofile.html', id=session.get('id'))
    else:
        return render_template('LoginPage.html', id='')
    
# 비밀번호 찾기 페이지 _이름으로
@app.route('/findpw_nm')
def findpw_nm():
    return render_template('findpw_nm.html', id=LogOnOff())


# 비밀번호 찾기 페이지 _이메일로 
@app.route('/findpw_em')
def findpw_em():
    return render_template('findpw_em.html', id=LogOnOff())

# 디자이너 소개 페이지
@app.route('/designer')
def designer():
    return render_template('DesignerIntro.html', id=LogOnOff())


@app.route('/searching_start', methods = ['POST', 'GET'])
def searching_start():
    session.pop('list', None)
    session.pop('what', None)
    return json.dumps('session out')

# 게시판 페이지
@app.route('/board/<number>', methods = ['POST', 'GET'])
def board(number):
    page = int(number[5])
    list =[]
    search=''
    # 최초 검색 시
    if number[11] == 'Q' and 'list' not in session :
        print('s3353g oin')
        search_sort = request.form['search_what_set']
        search = request.form['InputTextBox']
       
        category = request.form['category_set']
        CostDown = request.form['CostDown']
        CostUp = request.form['CostUp']
        
        deadline = request.form['DeadLineFilterInput']
        #over_include = request.form['DeadLineInclude']
        over_include=''
        show_sort = request.form['select_select']
        
        list = PostFilter(page, search_sort, search, category, CostDown, CostUp, deadline, over_include, show_sort)
        
        sort = 'QN'
        #page = len(list)
        if show_sort == 'Deadline':
            what = 'deadline'
        elif show_sort == 'HighCost':
            what = 'cost'
        else:
            what = 'no'
        session['list'] = list
        session['what'] = what
        list = SortByPage(page, what, list)
    #필터링 검색 페이지 넘길경우
    elif  number[11] == 'Q' and 'list' in session :
        #print('seesssing oin')
        list = session.get('list')
        what = session.get('what')
        list = SortByPage(page, what, list)
        print('seesssing oin')
        sort = 'QN'
    
    elif number[11] == 'C':
        # 최신순으로 정렬
        #list = SortByPage(page, 'no', '')
        session.pop('list', None)
        session.pop('what', None)
        
        db=db_connect()
        cursor = db.cursor()
        
        cursor.execute("select count(*) from post")
        count = int(cursor.fetchone()[0])
        
        cursor.execute("select no from post order by no desc limit %s, %s" %( (page-1) * 10, 10)) 
        
        PostList=[]  # 게시판 화면에 출력할 게시글 no를 리스트에 저장
        for i in cursor.fetchall():
            PostList.append(i[0])
            
        now_date = TimeNow()
        
        for no in PostList:
            cursor.execute("SELECT no, name, title, deadline, upload_date, cost, `show`, hurry, dat_count, id_value\
                from post WHERE no=%s" %no)
            post=[]
            one_post = cursor.fetchone()
            for i in range(10):
                if i == 3 : # 날짜 문자열 변환, 마감일자
                    day = CountDeadline(str(now_date)[:10], str(one_post[i]))
                    post.append(day)
                elif i == 4: #작성일자
                    date = str(one_post[i])
                    
                    NewPost = CountTime(one_post[i])
                    date = date[:4]+'.'+date[5:7]+'.'+date[8:10]
                    post.append(date)
                else:
                    post.append(one_post[i])
            
            post.append(NewPost)
            list.append(post)
        
        cursor.close()
        db.close()
        
        list = [list, count]
        
        print('current')
        sort = 'CN'
    
    #총 페이지 개수
    count = int(list[1] /10) +1
    #페이지 개수가 10의 배수일 경우 페이지를 하나 줄여줌
    if int(list[1] %10) ==0:
        count -=1
    
    return render_template('board.html', id=LogOnOff(), post= list[0], PageCount = count, page=page, sort=sort + search)

#게시글 필터 
def PostFilter(page, what, search, category, CostDown, CostUp, deadline, over_include, show_sort):
    #now_date = TimeNow()
    all=''
    db=db_connect()
    cursor = db.cursor()
    if what == 'all':#제목+내용일 때
        what = 'title'
        all = 'all'
    # 카테고리 분리
    category_list = category.split('#')
    del category_list[0]
    
    search = search.replace(' ','')
    a =0
    k=0
    PostList=[]
    # 카테고리 검색
    if len(category_list) >0:
        for hash in category_list:
            cursor.execute("select no from (select no from post \
            where category like '%s' ) s" %(  "%" +hash+ "%")) 
            
            hash_list=[]
            a=1
            for i in cursor.fetchall():
                hash_list.append(i[0])
            #if k>0:
            #    PostList = set(hash_list) & set(PostList)
            #else:
            PostList = set(hash_list)
            
            k+=1
        
    #검색내용 서칭 
    if len(search)>0:
        cursor.execute("select no from (select no from post \
            where %s like '%s' ) s" %( what, "%" +search+ "%")) 
        
        search_list=[]  # 게시판 화면에 출력할 게시글 no를 리스트에 저장
        for i in cursor.fetchall():
            search_list.append(i[0])
        if a==1:
            PostList = set(search_list) & set(hash_list)
        else:
            PostList = set(search_list)
        a=2
        print(PostList)
        
    #제목+내용일 때
    if all =='all' and len(search)>0: #제목+내용일때
        cursor.execute("select no from (select no from post \
            where %s like '%s' ) s" %( 'content', '%' +search+ '%')) 
        for i in cursor.fetchall():
            search_list.append(i[0])
            
        PostList = set(search_list) & set(PostList)
    
    # 가격 범위 검색, 가격 값 없으면 최소/최대값으로 변경
    if CostDown != '' or CostUp != '':
        if CostDown=='':
            CostDown = 0
        elif CostUp=='':
            CostUp = 99990000
            
        cost_list=[]
        cursor.execute("select no from (select no from post where cost > %s AND cost < %s) s" %(CostDown, CostUp)) 
        for i in cursor.fetchall():
            cost_list.append(i[0])
        if a==1:
            PostList = set(hash_list) & set(cost_list)
            
        elif a==2:
            PostList = set(search_list) & set(cost_list)
            
        else:
            PostList = set(cost_list)
            
        a=3
    #마감날짜 검색
    if deadline != '':
        deadline_list=[]
        cursor.execute("select no from (select no from post where deadline > '%s' ) s" %deadline) 
        for i in cursor.fetchall():
            deadline_list.append(i[0])
            
        if a==1:
            PostList = set(hash_list) & set(deadline_list)
        elif a==2:
            PostList = set(search_list) & set(deadline_list)
        elif a==3:
            PostList = set(deadline_list) & set(cost_list)
        else:
            PostList = set(deadline_list)
            
    # 내림차순 정렬
    list(PostList).sort(reverse=True) 
    
    cursor.close()
    db.close()
    return list(PostList)


#게시글 정렬, what 은 뭘로정렬하는지 
def SortByPage(page, what, list):
    db=db_connect()
    cursor = db.cursor()
    
    #페이지 번호 통해서 DB 데이터 불러오는 시작점 계산
    """
    page = (page-1) * 10
    cursor.execute("select no from (select no from post order by %s desc limit %s, %s) s" %( what, page, 10)) 
    PostList=[]  # 게시판 화면에 출력할 게시글 no를 리스트에 저장
    for i in cursor.fetchall():
        num = i[0]
        PostList.append(num)
    """
    print(list)
    sort_dic={} 
    pagenum = (page-1) * 10
    # 정렬만 필터링 할 경우
    if len(list) ==0:
        cursor.execute("select no from \
                    (select no from post order by %s desc limit %s, %s) s" %( what, pagenum, 10)) 
        sort_list=[]  # 게시판 화면에 출력할 게시글 no를 리스트에 저장
        for i in cursor.fetchall():
            sort_list.append(i[0])
        print(sort_list)
        cursor.execute("select count(*) from post")
        count = int(cursor.fetchone()[0])
    # 뭐든지 필터링을 할 경우
    else:
        for num in list:
            cursor.execute("select %s from post where no= %s" %( what, num)) 
             # 게시판 화면에 출력할 게시글 no를 리스트에 저장
            sort_dic[num] = cursor.fetchone()[0]
    
        sorted_dic = dict(sorted(sort_dic.items(), key=operator.itemgetter(1), reverse=True))
        print(sorted_dic)
        count = len(sorted_dic)
    
        sort_list = sorted_dic.keys()
    
    PrintPost=[]
    j=0
    k=0
    now_date = TimeNow()
    for no in sort_list:
        if j>=pagenum:
            sql = "SELECT no, name, title, deadline, upload_date, cost, `show`, hurry, dat_count, id_value\
                    from post WHERE no=%s"
            cursor.execute(sql, no)
            post=[]
            one_post = cursor.fetchone()
            for i in range(10):
                if i == 3 : # 날짜 문자열 변환, 마감일자
                    day = CountDeadline(str(now_date)[:10], str(one_post[i]))
                    post.append(day)
                elif i == 4: #작성일자
                    date = str(one_post[i])
                    NewPost = CountTime(one_post[i])
                    date = date[:4]+'.'+date[5:7]+'.'+date[8:10]
                    post.append(date)
                else:
                    post.append(one_post[i])
                
            post.append(NewPost)
            PrintPost.append(post)
            k+=1
        if k>=9:
            break
        
        j+=1
    cursor.close()
    db.close()
    print(PrintPost)
    return [PrintPost, count]

    
#게시글 하나 보여줄때 DB에서 정보 불러오기
def Post_Print(num):
    print('=====')
    post =[]
    
    db=db_connect()
    cursor = db.cursor()
    
    cursor.execute( " SELECT * FROM post WHERE no = %s " %num) 
    for one in cursor.fetchone():
        post.append(one)
    
    cursor.close()
    db.close()
    
    #마감일은 날짜만 긁어서 계산
    #deadline = str(post[4])[:10]
    post[4] = str(post[4])[:10]
    #해쉬태그는 #로 분해 후 저장
    hash = post[7].split('#')
    del hash[0]
    post[7] = hash
    #업로드날짜도 날짜만 긁어서 계산
    post[9] =str(post[9])[:10]
    #이미지 파일은 ?로 분리
    img = post[10].split('?')
    del img[-1]
    if img[0] == '':
        img='no_pic'
    post[10] = img
    
    return post

# 게시글 보여주기 함수
@app.route('/post/<NameNum>')
def ShowPost(NameNum):
    # 불러온 정보를 통해 게시글 작성자 아이디와 게시글 번호를 입력
    post_no = NameNum.split('%$')[1]
    #조회 추가
    db=db_connect() 
    cursor = db.cursor()
    #조회수 긁어와서 1추가후 다시 입력
    cursor.execute("SELECT `show` FROM post where no='%s' " %post_no)
    show = int(cursor.fetchone()[0])
    cursor.execute("UPDATE post SET `show`='%s' WHERE no='%s' " %(str(show+1), post_no))
    
    cursor.close()
    db.commit()
    db.close()
    
    # 해당 게시글 모든 정보 데이터베이스에서 불러오기
    post = Post_Print(post_no)
    comment = ShowComment(post_no)
    
    return render_template('ShowPost.html', id=LogOnOff(), post=post, comment_list = comment )

# 댓글 작성 함수
@app.route('/input_comment', methods = ['POST', 'GET'])
def input_comment():
    if request.method == 'POST':
        star = request.form['star']
        PostNo = request.form['PostNo']
        comment = request.form['comment']
        
        if comment.replace(' ','') == '':
            return json.dumps('')
        
        comment_list = CommentDB(PostNo, comment, star, 'yes')
        if comment_list == 91:
            return json.dumps('91')
        db=db_connect() 
        cursor = db.cursor()
        cursor.execute("SELECT no FROM %s order by no desc limit 1" %('comment'+PostNo))
        comment_num = cursor.fetchone()[0]
        cursor.close()
        db.close()
        comment_list.append(comment_num)
        return json.dumps( comment_list )
        
# 답글 작성 함수
@app.route('/input_reply', methods = ['POST', 'GET'])
def input_reply():
    if request.method == 'POST':
        PostNo = request.form['PostNo']
        comment = request.form['comment']
        comment_num = request.form['comment_num']
        
        if comment.replace(' ','') == '':
            return json.dumps('')
            
        comment_list = CommentDB(PostNo, comment, 'of', comment_num)
        if comment_list == 91:
            return json.dumps('91')
        comment_list.append(comment_num)
        return json.dumps(comment_list)
        
        
def CommentDB(PostNo, comment, star, org):
    id = LogOnOff()
    if id== '':
        return 91
    
    date = TimeNow()
    name = WhatYourName(id)
    
    db=db_connect() 
    cursor = db.cursor()
    cursor.execute("INSERT INTO %s (id_value, name, comment ,star, org_comment, date) \
          VALUES('%s', '%s', '%s', '%s', '%s', '%s')" %('comment'+PostNo, id, name, comment, star, org,date))
    
    #댓글 추가
    cursor.execute("UPDATE post SET dat_count=dat_count+1 WHERE no='%s' " % PostNo)

    cursor.close()
    db.commit()
    db.close()

    return [name, comment, star, org, str(date)]

#댓글 보여주기 함수
def ShowComment(PostNo):
    comment_list=[]
    db=db_connect() 
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM %s" %('comment'+PostNo))
    for one in cursor.fetchall():
        list=[]
        for i in range(2, 7):
            if str(type(one[i])) == "<class 'datetime.datetime'>":
                date = str(one[i])
                if date[:10] == str(TimeNow())[:10] :
                    day_input = "오늘 "+date[11:-3]
                else:
                    day_input = date[:10]
                list.append(day_input)
                
            elif i == 5: #원 댓글 여부
                if one[i] != 'yes':
                    list.append(int(one[i]))
                else:
                    list.append(one[i])
            else:
                list.append(one[i])
            
        # comment_number
        #포르필이미지 추가
        cursor.execute("SELECT profile_img FROM user WHERE id_value='%s'" %one[1] )
        list.extend([one[0], one[1], LogOnOff(), cursor.fetchone()[0]])
        comment_list.append(list)
        
    cursor.close()
    db.commit()
    db.close()
    
    return comment_list

# 게시판 페이지
@app.route('/signuppage')
def signuppage():
    return render_template('signUp.html', id=LogOnOff())
    
# 내 프로필 페이지
@app.route('/myprofile')
def myprofile():
    return render_template('myprofile.html', id=LogOnOff())

# 게시글 작성과 동시에 댓글 테이블 작성
def MakeCommentTable(num):
    db=db_connect() 
    cursor = db.cursor()
    cursor.execute("CREATE TABLE  %s( no bigint(10) unsigned NOT NULL auto_increment,\
            id_value varchar(30) not null, name varchar(30) ,\
            comment varchar(250), star varchar(5), org_comment varchar(5), date datetime,\
            primary key(no))" %('comment' + str(num)))
    cursor.close()
    db.commit()
    db.close()
    return 0

# 로그인 action
@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        id=request.form['idButton']
        pw=request.form['pwButton']
        
        db=db_connect()
        #DB를 열어서 존재하는 id 인지 판단
        cursor = db.cursor()
        cursor.execute( "SELECT EXISTS ( SELECT * FROM user WHERE  id_value='%s') as success" %id) 
        
        if cursor.fetchone()[0] == 0:
            print('login failed_no id')
            cursor.close()
            db.close()
            return "<script>alert('아이디가 존재하지 않습니다.');window.location.replace('/LoginPage');</script>"
            
        #else
        cursor.execute("SELECT password FROM user WHERE id_value='%s'" %id)
        pw_db = cursor.fetchone()[0]
        cursor.close()
        db.close()
        
        if pw == pw_db:
            print('login success')
            LogInSuccess(id)
            return render_template('myprofile.html', id=id)
            
        else:
            print('login failed_wrong pw')
            return "<script>alert('비밀번호가 일치하지 않습니다.');window.location.replace('/LoginPage');</script>"
            

# 회원가입 action
@app.route('/signup', methods = ['POST', 'GET'])
def SignUp():
    if request.method == 'POST':
        id=request.form['idSignUpButton']
        name=request.form['namdSignUpButton']
        pw=request.form['pwSignUpButton']
        pwc=request.form['pwRepeatSignUpButton']
        email=request.form['EmailSignUpButton']
        print(email)
        # id 검사
        # 5~20자의 영문 소문자, 숫자와 특수기호(_),(-)만 사용 가능합니다.
        idOK = idCheck(id)
        if idOK == 0 :
            return "<script>alert('id는 5~20사이만 가능합니다');window.location.replace('/signuppage');</script>"
        
        elif idOK == 101 :
            return "<script>alert('id에 공백을 입력할 수 없습니다.');window.location.replace('/signuppage');</script>"
        elif idOK == 202 :
            return "<script>alert('id에 특수문자를 입력할 수 없습니다.');window.location.replace('/signuppage');</script>"
        elif idOK == 303 :
            return "<script>alert('이미 존재하는 id 입니다.');window.location.replace('/signuppage');</script>"
        elif idOK == 100 :
            print('id success')
            
        nameOK = NameCheck(name)
        if nameOK == 0:
            return "<script>alert('이룸은 1~20 사이만 가능합니다');window.location.replace('/signuppage');</script>"
        elif nameOK == 202:
            return "<script>alert('이룸에 특수문자를 입력할 수 없습니다.');window.location.replace('/signuppage');</script>"   
        elif nameOK == 303:
            return "<script>alert('이미 존재하는 이름입니다.');window.location.replace('/signuppage');</script>"   
        elif nameOK == 100 :
            print('name success')
            
        PasswordOK = PasswordCheck(pw, pwc)
        if PasswordOK == 0:
            return "<script>alert('비밀번호는 8~20 사이만 가능합니다');window.location.replace('/signuppage');</script>"
        elif PasswordOK == 101:
            return "<script>alert('비밀번호에 공백을 입력할 수 없습니다.');window.location.replace('/signuppage');</script>"
        elif PasswordOK == 44:
            return "<script>alert('비밀번호 확인이 일치하지 않습니다.');window.location.replace('/signuppage');</script>"
        elif PasswordOK == 100:
            print('password success')
            
        EmailOK = EmailCheck(email)
        if EmailOK == 90:
            return "<script>alert('잘못된 이메일 형식입니다.');window.location.replace('/signuppage');</script>"
        elif EmailOK == 91:
            return "<script>alert('잘못된 이메일 형식입니다.');window.location.replace('/signuppage');</script>"
        elif EmailOK == 92:
            return "<script>alert('잘못된 이메일 형식입니다.');window.location.replace('/signuppage');</script>"
        elif EmailOK == 93:
            return "<script>alert('잘못된 이메일 형식입니다.');window.location.replace('/signuppage');</script>"
        elif EmailOK == 100:
            print('email success')
        
        print(email)
        SingUP_DB(id, name, pw, email)
        LogInSuccess(id)
        print('sign Up success')
        return "<script>alert('회원가입 성공');window.location.replace('/LoginPage');</script>"
# id 검사
# 5~20자의 영문 소문자, 숫자와 특수기호(_),(-)만 사용 가능합니다.      
def idCheck(id):
    chk = re.compile('[^0-9a-zA-Z_-]')
    
    # 5~20 자 이외의 문자열
    if len(id) > 20 or len(id) <5 :
        return 0
    # 공백 이외의 특수문자가 존재할 경우
    elif chk.search(id) != None:
        # 공백 존재할 경우
        if chk.search(id)[0] == ' ':
            return 101
        else:
            return 202
    else:
        # id 중복
        if exist_table('user', 'id_value', id) == 1:
            return 303
        # id 성공
        else:
            return 100
        
# 이름 검사 
# 1~20 자리, 숫자 특수문자 제외
def NameCheck(name):
    chk = re.compile('[^a-zA-Z가-힣 ]')
    
    if len(name) <1 or len(name) > 20:
        return 0
    # 공백 이외의 특수문자가 존재할 경우
    elif chk.search(name) != None:
        return 202
    else:
        # name 중복
        if exist_table('user', 'name', name) == 1:
            return 303
        # name 성공
        else:
            return 100

# password 검사
# 8~20자의 영문 소문자, 숫자와 특수문자 가능
def PasswordCheck(pw, pwc):
    # 비밀번호 확인이 일치하지 않을 경우
    if pw != pwc:
        return 44
    # 8~20 범위 밖의 비밀번호 입력
    elif len(pw)<8 or len(pw)>20:
        return 0
    # 비밀번호에 공백이 존재할 경우 
    elif ' ' in pw:
        return 101
    else: 
        return 100
    
# 이메일 검사 
# 이메일 형식 갖추고있는지, . 다음이 올바른 url 형식인지, 공백은 없는지 
def EmailCheck(email):
    # chk 는 로컬 형식, how는 도메인 주소 형식
    chk = re.compile("[^a-zA-Z0-9!#$%&'*+-/=?^_`{|}~]")
    how = re.compile('[^a-zA-Z0-9-]')
    # 최상위 도메인 리스트 
    lastDomainList=['com','net','org','int','edu','gov','mil','arpa', 'kr']
    # 이메일에 @가 2개이상 있거나 없을 경우 
    if len( email.split('@') ) != 2:
        print('too many @')
        return 90
    else:
        local = email.split('@')[0]
        domain = email.split('@')[1]
        if len( email.split('.') ) < 2:
            return 90
        
        lastdomain = domain.split('.')[-1]
        domain = domain.split('.')[0]
        
    if chk.search(local) != None:
        print('email lacal')
        return 91
    elif how.search(domain) != None:
        print('email domain')
        return 92
    else:
        for i in lastDomainList:
            if lastdomain == i:
                return 100
        
        return 93
    
## 회원가입 정보 데이터베이스에 입력
def SingUP_DB(id, name, pw, email):
    
    db=db_connect()                    
    cursor = db.cursor()
    date = TimeNow()
    
    sql = "INSERT INTO user (id_value, name, password ,email, signup_date)\
          VALUES(%s, %s, %s, %s, %s)"
          
    cursor.execute(sql, (id, name, pw, email, date))
    cursor.close()
    db.commit()
    db.close()
    return 0
        
### 로그인 세션 - 세션에 아이디 정보 저장
def LogInSuccess(id):
    session['id'] = id
    print('session in')
    return True

# log out
@app.route('/logout')
def LogOut():
    print('seesion out!!')
    session.pop('id', None)
    return render_template('LoginPage.html', id='')

# 글쓰기
@app.route('/WriteOnBoard', methods = ['POST', 'GET'])
def WriteOnBoard():
    if request.method == 'POST':
       # id = session.get('id')
        id = LogOnOff()
        if id== '':
            return "<script>alert('로그인 후 글을 작성해주세요.');window.location.replace('/LoginPage');</script>"
        title = request.form['WriteTitleInput']
        deadline  = request.form['DateInput']
        category = request.form['HashList_write']
        
        # 카테고리 개수 제한, 필수 입력이며, 최대 3개로 제한
        category_len = len(category.split('#') )
        if category_len < 2:
            return "<script>alert('카테고리는 필수입력입니다.');window.location.replace('/board');</script>"
        elif category_len > 4:
            return "<script>alert('카테고리는 최대 3개입니다.');window.location.replace('/board');</script>"
        
        cost = request.form['CostInput']
        # 가격 값은 순수한 숫자로만 이루어져있는지 판단 
        if cost.isdigit() == False:
            return "<script>alert('가격을 제대로 입력해주세요.');window.location.replace('/board');</script>"
        else:
            cost = int(cost)
            
        hurry_list = request.form.getlist('HurryUpCheckBox')
        content = request.form['WritingContent']
        upload_date = TimeNow()
        img_list=''
        name = WhatYourName(id)
        
        f_list = request.files.getlist('ImgUpload_write')
        print(f_list)
        # 아래 맨앞에 붙일것 : str(upload_date)[11:13]+'-'+
        img_date = str(upload_date)[14:16]+'-'+str(upload_date)[17:19]
        print(img_date)
        # 이미지 이름을 리스트로 만들어주는 조건문
        if len(f_list) >1:
            for i in f_list:
                f_name = secure_filename(i.filename)
                print(f_name)
                file_save_name = img_date+'_'+id+'_'+f_name[-5:]
                img_list = img_list+file_save_name+'?'
                
                # 업로드 분,초 + 아이디 + 원래이름
                i.save("./static/post_img/" + file_save_name)
        else:
            f_name = secure_filename(f_list[0].filename)
            f_name.save("./static/post_img/" + img_date+'_'+id+'_'+f_name[-5:])
            img_list = img_date+'_'+id+'_'+f_name[-5:]+'?'
            
        print(img_list)
        ## 한글 이미지 올리면 저장하기
        if ImgFileCheck(img_list) == 0 :
            return "<script>alert('이미지 파일을 불러오세요.');window.location.replace('/board');</script>"
        # 급구 체크 되어있을 경우
        if len(hurry_list) >0: 
            hurry = hurry_list[0]
        else: #급구 체크 아닐경우
            hurry = 'off'
        
        #write_date -- date now로 값 주기
        print(category)
        print(title)
        print(cost)
        print(deadline)
        print(hurry)
        
        db=db_connect()
        cursor = db.cursor()
        
        sql = """INSERT INTO post (id_value, name, title, deadline, 
                cost, hurry, category, content, upload_date, img, star, `show`, dat_count)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 0, 0, 0)"""
        
        cursor.execute(sql, (id, name, title, deadline, cost, hurry, category, content, upload_date, img_list))
        cursor.execute("select no from post order by no desc limit 1")
        post_number = cursor.fetchone()[0]
        
        cursor.close()
        db.commit()
        db.close()
        
        MakeCommentTable(post_number)
        PrintPost = Post_Print(post_number)
        
        
        return render_template('ShowPost.html', id=id, post= PrintPost)

# 비밀번호 찾기 action
@app.route('/findpw_email', methods = ['POST', 'GET'])
def findpw_email():
    if request.method == 'POST':
        id=request.form['idFindPwButton']
        email=request.form['EmailFindPwButton']
        
        pw = FindPassword(id, email, 'email')
        
        if pw==0:
            return "<script>alert('존재하지 않는 아이디입니다.');window.location.replace('/findpw_em');</script>"
        elif pw==1:
            return "<script>alert('존재하지 않는 이메일입니다.');window.location.replace('/findpw_em');</script>"
        else:
            pw = pw[:3] + '**' + pw[5:]
            return render_template('findpw_em.html', pw=pw, cont=100)

# 비밀번호 찾기 action
@app.route('/findpw_name', methods = ['POST', 'GET'])
def findpw_name():
    if request.method == 'POST':
        id=request.form['idFindPwButton']
        name=request.form['namdFindPwButton']
        
        pw = FindPassword(id, name, 'name')
        
        if pw == 0:
            return "<script>alert('존재하지 않는 아이디입니다.');window.location.replace('/findpw_nm');</script>"
        elif pw==1:
            return "<script>alert('존재하지 않는 이름입니다.');window.location.replace('/findpw_nm');</script>"
        else:
            pw = pw[:3] + '**' + pw[5:]
            return render_template('findpw_nm.html', pw=pw, cont=100)
        
# 비밀번호 찾기 함수 
def FindPassword(id, other, what):
    db=db_connect()
    #DB를 열어서 아이디가 있는지 판단
    cursor = db.cursor()
    cursor.execute( "SELECT EXISTS ( SELECT * FROM user WHERE  id_value='%s') as success" %id)    
    
    if cursor.fetchone()[0] == 0:
        print('no id')
        cursor.close()
        db.close()
        return 0
    
    cursor.execute( "SELECT EXISTS ( SELECT * FROM user WHERE  '%s'='%s') as success" %(what, other))   
    
    if cursor.fetchone()[0] == 0:
        print('no email')
        cursor.close()
        db.close()
        return 1
    
    else:
        cursor.execute( " SELECT password from user where id_value ='%s' " %id)
        pw = cursor.fetchone()[0]
        cursor.execute( " SELECT password from user where '%s' ='%s' " %(what, other))
        pwc = cursor.fetchone()[0]
            
    
    cursor.close()
    db.close()
    
    if pw ==  pwc:
        print(pw)
        return pw
    

# 댓글 답글 삭제
@app.route('/comment_delete', methods = ['POST', 'GET'])
def comment_delete():
    if request.method == 'POST':
        CommentNumber  = request.form['CommentNumber']
        PostNumber = request.form['PostNumber']
        tablename = 'comment' + PostNumber
        
        db=db_connect() 
        cursor = db.cursor()
        
        cursor.execute("SELECT org_comment FROM %s WHERE no=%s" %(tablename, CommentNumber) )
        
        # 원댓글일 경우
        if cursor.fetchone()[0]=='yes':
            cursor.execute("UPDATE %s SET comment='삭제된 댓글입니다' WHERE no=%s" %(tablename, CommentNumber) )
        else:  # 답글일 경우
            cursor.execute("DELETE FROM %s WHERE no=%s" %(tablename, CommentNumber) )
        
        #댓글 읽어오기
        cursor.execute("UPDATE post SET dat_count=dat_count-1 WHERE no='%s' " %PostNumber)
        #삭제된 댓글이라고 표시
        cursor.execute("UPDATE %s SET star='%s' WHERE no='%s' " %(tablename, 'de',CommentNumber))
        
        cursor.close()
        db.commit()
        db.close()
        
        return json.dumps('delete')
        
# 댓글 답글 수정
@app.route('/comment_fix', methods = ['POST', 'GET'])
def comment_fix():
    if request.method == 'POST':
        CommentNumber  = request.form['CommentNumber']
        PostNumber = request.form['PostNumber']
        new_comment = request.form['new_comment']
        
        db=db_connect() 
        cursor = db.cursor()
        
        cursor.execute("UPDATE %s SET comment='%s' WHERE no=%s"\
                        %('comment' + PostNumber, new_comment, CommentNumber) )
        
        cursor.close()
        db.commit()
        db.close()
        
        return json.dumps(new_comment)
        
# 게시글 삭제
@app.route('/post_delete', methods = ['POST', 'GET'])
def post_delete():
    if request.method == 'POST':
        PostNumber  = request.form['PostNumber']
        
        db=db_connect() 
        cursor = db.cursor()
        
        cursor.execute("DROP TABLE %s" %('comment'+PostNumber) )
        cursor.execute("DELETE FROM post WHERE no=%s" %PostNumber )
        
        cursor.close()
        db.commit()
        db.close()
        print('post delete complete')
        return json.dumps('')
        
        
        
if __name__ == '__main__':
    app.run(host = "0.0.0.0", debug = True)
    
    