// beaudeer project javascript file


var HashTagList = new Array();
HashTagList = ['web', 'char', 'ppt', 'poster'];



/**********  로그인 돌아가기 버튼 누르면   *********/
$('#Back2LoginPage, #Back2LoginPageFromFindPw').click(function(){
	//$('#SignUpPage').css('display', 'none');
	$('#LoginPage').css('display', 'block');
	$('#FindPwPage').css('display', 'none');
	$('#FindPwSelectPage').css('display', 'none');
});
/**********  비밀번호찾기 버튼 누르면   *********/
$('#FindPwButton').click(function(){
	//$('#SignUpPage').css('display', 'none');
	$('#LoginPage').css('display', 'none');
	$('#FindPwPage').css('display', 'none');
	$('#FindPwSelectPage').css('display', 'block');
});

$('.DesignerSpecialHash#ooooooo').click(function(){
	console.log('efe');
	$('.AllDesignerIntroducePage').css('display', 'none');
	$('.OneDesignerIntroducePage').css('display', 'block');
});
$('.BackDesignerButton').click(function(){
	$('.AllDesignerIntroducePage').css('display', 'block');
	$('.OneDesignerIntroducePage').css('display', 'none');
});

/* 글쓰기 버튼 클릭 화면*/
$('#WritingButton').click(function(){
	$('.BoardInside').css('display', 'none');
	$('.WritingPage').css('display', 'block');
});
/* 로그인 화면으로 돌아가기  */
$('#Back2BoardButton').click(function(){
	$('.BoardInside').css('display', 'block');
	$('.WritingPage').css('display', 'none');
	
	// 작업 도중 내용 모두 제거
	$('.WritingContent').val('');
	$('#WriteTitleInput').val('');
	$('.DateInput').val('');
	$('.CostInput').val('');
	$('input[name=HurryUpCheckBox]').prop('checked', false);
	HashColorOrg();
});


function PasswordComfirm(){

	var pw1 = document.getElementById('pwSignUpButton').value;
	var pw2 = document.getElementById('pwRepeatSignUpButton').value;
	
	if (pw2 == "" || pw1 ==""){   //아무것도 입력되지 않았을때
		document.getElementById('pw_confirm_result').innerHTML="";
		return 2;
	}

	
	else if (pw1 == pw2) {  // 비밀번호 일치
		document.getElementById('pw_confirm_result').innerHTML="일치합니다.";
		document.getElementById('pw_confirm_result').style.color ='blue';
		return 100;
	}
	
	else{  //비밀번호 불일치
		document.getElementById('pw_confirm_result').innerHTML="일치하지 않습니다.";
		document.getElementById('pw_confirm_result').style.color ='red';
		return 0;
	}
}


// PPT 해쉬태그
$('#Hash_ppt_bt').click(function(){
	if($('#Hash_ppt').text() == ''){
		$('#Hash_ppt_bt').css('background-color', 'orange');
		$('#Hash_ppt').text( $('#Hash_ppt_bt').attr('value') );
		//$('#Hash_ppt_bt').css('online', 'none');
	}
	else{
		$('#Hash_ppt_bt').css('background-color', '#F7C2C2');
		$('#Hash_ppt').text( '');
	}
	//console.log($('#Hash_ppt_bt').attr('value'));
});
// 웹 해쉬태그
$('#Hash_web_bt').click(function(){
	if($('#Hash_web').text() == ''){
		$('#Hash_web_bt').css('background-color', 'orange');
		//$('#Hash_web_bt').css('online', 'none');
		$('#Hash_web').text( $('#Hash_web_bt').attr('value') );
		console.log($('#Hash_web_bt').attr('value'));
	}
	else{
		$('#Hash_web_bt').css('background-color', '#F7C2C2');
		$('#Hash_web').text( '' );
	}
});

// 캐릭터 해쉬태그 
$('#Hash_char_bt').click(function(){
	console.log("why");
	//alert("wjj");
	if($('#Hash_char').text() == ''){
		$('#Hash_char_bt').css('background-color', 'orange');
		$('#Hash_char').text( $('#Hash_char_bt').attr('value') );
		console.log($('#Hash_char_bt').attr('value'));
	}
	else{
		$('#Hash_char_bt').css('background-color', '#F7C2C2');
		$('#Hash_char').text( '' );
	}
});
// 포스터 해쉬태그 
$('#Hash_poster_bt').click(function(){
	if($('#Hash_poster').text() == ''){
		$('#Hash_poster_bt').css('background-color', 'orange');
		$('#Hash_poster').text( $('#Hash_poster_bt').attr('value') );
		console.log($('#Hash_poster_bt').attr('value'));
	}
	else{
		$('#Hash_poster_bt').css('background-color', '#F7C2C2');
		$('#Hash_poster').text( '' );
	}
});


// 댓글 별 누르면 input에 입력
$('.CommentStarButton').click(function(){
	
	var value =$('.CommentStarOnOff').attr('value') ;
	
	if(value.slice(-2) == 'of'){
		$('.CommentStarOnOff').attr( 'value', value.slice(0,-2)+'on' );
		$('#CommentOneStarImg_input').attr("src", "/static/star.jpg");
	}
	else{
		$('.CommentStarOnOff').attr( 'value', value.slice(0,-2)+'of' );
		$('#CommentOneStarImg_input').attr("src","/static/star_empty.png");
	}
});

// 댓글 입력하면 ajax로 전송 후 화면에 출력 ---- 댓글 입력했을 때
//댓글 최상단 입력 버튼에 온클릭 함수
function CommentInput(){
	//alert("1");
	var star = $('.CommentStarOnOff').attr('value').slice(-2);
	var comment = $('.CommentInput').val();
	var PostNo = $('.CommentStarOnOff').attr('value').slice(0, -2);
	//console.log(comment+'-'+PostNo+'--'+star);
	$('.CommentInput').val('');
	$.ajax({
		url:'/input_comment',
		type: 'POST',
		dataType: 'json',
		data: {
			'star': star, 
			'comment': comment,
			'PostNo': PostNo
			},
		
		success : function (data){
			//alert(data);
			if(data == ''){
					alert('뭐라도 입력하세요.');
			}
			else if(data==91){
				alert('로그인좀 해라');
				window.location.href="/LoginPage";
			}
			else{
				ShowComment(data);
				//별 초기화
				var value =$('.CommentStarOnOff').attr('value') ;
				$('.CommentStarOnOff').attr( 'value', value.slice(0,-2)+'of' );
				$('#CommentOneStarImg_input').attr("src","/static/star_empty.png");
			}
		}
	});
}

// 댓글 보여주는 출력 함수 
function ShowComment(data){
	var box = document.createElement( "div" ); 
	box.className = "CommentLine";
	box.id = "CommentLine"+data[5];
	//alert("hello");
	var inner_box = document.createElement( "div" ); 
	inner_box.className = "CommentBoard";
	
	var img = document.createElement('img'); 
	img.className = "CommentProfileImg";
	img.setAttribute("src", "/static/taeli.jpg");
	//img.setAttribute("style", "margin: 1px 9px");
	
	var text_box = document.createElement('div'); 
	text_box.className = "CommentTextBox";
	
	var CommentHeadBox = document.createElement('div'); 
	CommentHeadBox.className = "CommentHeadBox";
	
	var name = document.createElement('span'); 
	name.className = "CommentName";
	name.innerHTML= data[0];
	
	var comment = document.createElement('div'); 
	comment.className = "CommentText";
	comment.innerHTML= data[1];
	
	var under_cmt = document.createElement('button'); 
	under_cmt.className = "WannaCommentAgain";
	under_cmt.setAttribute("name","reply_input_"+data[5]);
	under_cmt.setAttribute("id","reply_input_"+data[5]);
	under_cmt.innerHTML= "답글 달기";
	
	var day_ago = document.createElement('div'); 
	day_ago.className = "CommentDate";
	day_ago.innerHTML= "오늘 "+data[4].slice(10, 16);
	
	var reply = document.createElement( "input" ); 
	reply.className = "ReplyComment";
	reply.id = "Reply_Comment"+data[5];
	reply.setAttribute("type","text");
	reply.setAttribute("placeholder","답글 작성");
	
	var reply_box = document.createElement( "div" ); 
	reply_box.className = "ReplyHideBox";
	reply_box.setAttribute("style","display: none");
	reply_box.setAttribute("id","ReplyComment"+data[5]);
	
	var reply_bt = document.createElement('button'); 
	reply_bt.className = "ReplyButton";
	reply_bt.innerHTML= "입력";
	reply_bt.setAttribute("id","ReplyInputButton"+data[5]);
	reply_bt.setAttribute("name","ReplyInputButton");
	
	var mycomment = document.createElement('div'); 
	mycomment.className = "MyCommentBox";
	
	var fix = document.createElement('span'); 
	fix.className = "MyCommentFix";
	fix.innerHTML= "수정";
	
	var del = document.createElement('span'); 
	del.className = "MyCommentDel";
	del.innerHTML= "삭제";
	
	var star_onoff = data[2].slice(-2);
	if(star_onoff == 'on'){
		var star = document.createElement('img'); 
		//star_img.setAttribute("class", "CommentOneStarImg");
		star.className = "CommentOneStarImg";
		star.setAttribute("src", "/static/star.jpg");
	}else{
		var star = document.createElement('div'); 
		star.className = "CommentOneStar";
	}
	
	
	inner_box.appendChild(star);
	inner_box.appendChild(img);
	inner_box.appendChild(text_box);
	inner_box.appendChild(reply_box);
	
	CommentHeadBox.appendChild(name);
	CommentHeadBox.appendChild(day_ago);
	text_box.appendChild(CommentHeadBox);
	text_box.appendChild(comment);
	
	CommentHeadBox.appendChild(under_cmt);
	CommentHeadBox.appendChild(mycomment);
	
	mycomment.appendChild(fix);
	mycomment.appendChild(del);
	
	reply_box.appendChild(reply);
	reply_box.appendChild(reply_bt);
	box.appendChild(inner_box);
	document.getElementById('CommentOneBox').appendChild(box);
}

//답글달기 버튼 클릭, class이름을 인자로 받음
function reply_input(comment, PostNumber, comment_num){
	//var comment_len = comment.length;
	if(comment.length != 0){
		$.ajax({
			url:'/input_reply',
			type: 'POST',
			dataType: 'json',
			data: {
				'comment': comment,
				'PostNo': PostNumber,
				'comment_num': comment_num
				},
			
			success : function (data){
				console.log(data);
				
				if(data == ''){
					alert('뭐라도 입력하세요.');
				}
				else if(data==91){
					alert('로그인좀 해라');
					window.location.href="/LoginPage";
				}
				else{
					var box = document.createElement( "div" ); 
					//var arrow = document.createElement( "div" ); 
					var out_box = document.createElement('div'); 
					var inner_box = document.createElement('div'); 
					var star = document.createElement('div'); 
					var name = document.createElement('span'); 
					var mycomment = document.createElement('div'); 
					var fix = document.createElement('span'); 
					var del = document.createElement('span'); 
					var date = document.createElement('div'); 
					var comment = document.createElement('div'); 
					var img = document.createElement('img'); 
					
					box.className = "CommentReplyBox";
					out_box.className = "CommentBoard";
					inner_box.className = "CommentTextBox";
					star.className = "CommentOneStar";
					name.className = "CommentName";
					comment.className = "CommentText";
					date.className = "CommentDate";
					img.className = "CommentProfileImg";
					mycomment.className = "MyCommentBox";
					fix.className = "MyCommentFix";
					del.className = "MyCommentDel";
					star.setAttribute("id","ReplyArrow");
					img.setAttribute("style", "margin: 0px 9px");
					//img.setAttribute("style", "margin-right: 13px");
					
					star.innerHTML= "↳";
					fix.innerHTML= "수정";
					del.innerHTML= "삭제";
					comment.innerHTML= data[1];
					name.innerHTML= data[0];
					date.innerHTML= "오늘 " + data[4].slice(11,16);
					img.src='/static/dahyun.jpg';
					//arrow.innerHTML= "↳";
					
					out_box.appendChild(box);
					box.appendChild(star);
					box.appendChild(img);
					box.appendChild(inner_box);
					inner_box.appendChild(name);
					//box.appendChild(under_link);
					inner_box.appendChild(date);
					inner_box.appendChild(mycomment);
					mycomment.appendChild(fix);
					mycomment.appendChild(del);
					inner_box.appendChild(comment);
					document.getElementById('CommentLine'+data[5]).appendChild(out_box);
					
					$('#ReplyComment'+data[5]).css('display', 'none');
					$('#Reply_Comment'+data[5]).val('');
					$('#ReplyInfo').attr( 'value', '' );
				}
			}
		});
	}
	
}

// 댓글 삭제
$('.MyCommentDel').click(function(){
	console.log('del');
	var box_name = $(this).parent().parent().parent().parent().attr('class');
	//var box = $(this).parent().parent().parent();
	//console.log(box_name);
	// 답글 삭제 경우
	var CommentNumber = "";
	if(box_name == 'CommentReplyBox'){
		$(this).parent().parent().parent().parent().parent().css('display', 'none');
		CommentNumber = $(this).parent().parent().parent().attr('id');
		CommentNumber = CommentNumber.slice(6,);
	}
	// 댓글 삭제 경우
	else {
		$(this).parent().parent().parent().children('.CommentText').text('삭제된 댓글입니다.');
		CommentNumber = $(this).parent().parent().parent().parent().parent().attr('id');
		console.log(CommentNumber);
		CommentNumber = CommentNumber.slice(11,);
	}
	var PostNumber = $('#PostNumber').text();
	console.log(PostNumber);
	console.log('-');
	console.log(CommentNumber);
	
	$.ajax({
			url:'/comment_delete',
			type: 'POST',
			dataType: 'json',
			data: {
				'CommentNumber': CommentNumber,
				'PostNumber': PostNumber
				},
			
			success : function (data){
				console.log('delete success');
			}
	});
});

// 댓글 수정
$('.MyCommentFix').click(function(){
	var box_name = $(this).parent().parent().parent().parent().attr('class');
	var org_comment = $(this).parent().parent().parent().children('.CommentText').text();
	$(this).parent().parent().parent().children('.CommentText').css('display', 'none');

	var box = document.createElement( "div" ); 
	var input = document.createElement( "input" ); 
	//var input_save = document.createElement( "input" ); 
	var button = document.createElement( "button" ); 
	var cancle = document.createElement( "button" ); 
	
	// 답글 수정 경우
	if(box_name == 'CommentReplyBox'){
		var CommentNumber = $(this).parent().parent().parent().attr('id');
		CommentNumber = CommentNumber.slice(6,);
		//console.log(CommentNumber)
	}
	// 댓글 수정 경우
	else {
		var CommentNumber = $(this).parent().parent().children('button').attr('id');
		CommentNumber = CommentNumber.slice(12,);
		//console.log(CommentNumber)
	}
	
	var org_fix_num = $('.FixSave').text();
	
	if( org_fix_num != CommentNumber){
		//console.log(org_fix_num)
		
		$('#ReplyComment'+org_fix_num).parent().prev().css("display", "block");
		$('#ReplyComment'+org_fix_num).parent().remove();
		//$('#ReplyComment'+org_fix_num).parent().prev().css("display", "block");
		console.log('etdd')
		$('.FixSave').text(CommentNumber);
	
		
		input.className = "ReplyComment";
		input.id = "ReplyComment"+CommentNumber;
		button.className = "ReplyFixButton";
		cancle.className = "ReplyCancleButton";
		box.className = "ReplyFixBox";
		//input_save.className = "Reply_save";
		//input_save.setAttribute('style', 'display: none');
		
		input.setAttribute('value', org_comment);
		button.innerHTML= "수정";
		cancle.innerHTML= "취소";
		//input_save.innerHTML= org_comment;
		box.appendChild(input);
		box.appendChild(cancle);
		box.appendChild(button);
		$(this).parent().parent().parent().parent().children('.CommentTextBox').append(box);
	
}
});

//댓글 수정 함수
function CommentModify(new_comment, CommentNumber){
		//var new_comment = input.innerHTML;
		
		var PostNumber = $('#PostNumber').text();
		//var new_comment = input.innerHTML;
		console.log(new_comment);
		
		$.ajax({
				url:'/comment_fix',
				type: 'POST',
				dataType: 'json',
				data: {
					'CommentNumber': CommentNumber,
					'PostNumber': PostNumber,
					'new_comment': new_comment
					},
				
				success : function (data){
					console.log('fis success');
					
				}
		});
	return new_comment
};

//게시글 삭제 버튼---아무나 삭제 못하게 막기
$('.PostDeleteButton').click(function(){
	//console.log('tt');
	var PostNumber = $('#PostNumber').text();
	console.log(PostNumber);
	
	$.ajax({
				url:'/post_delete',
				type: 'POST',
				dataType: 'json',
				data: {
					'PostNumber': PostNumber
					},
				
				success : function (data){
					console.log('post delete success');
					window.location.replace('/board/%&2$%1$@7&1C45^8E85');
				}
		});
	
});
	



//  글쓰기  form   해쉬태그 모음을 문자열로 바꾸기
function WriteHash(){
	
	console.log(HashTagList);
	var HashList = ''
	for(var i=0; i<HashTagList.length; i++){
		var Hash = HashTagList[i];
		var plus = $('#Hash_'+Hash).text();
		//var HashName = 'Hash_' + Hash;
		HashList=HashList +plus;
		
	}
	$('.HashList_write').val(HashList);
	
	return true
}

//   글쓰기 도중 뒤로가기 할 때, 해쉬태그 버튼 색 전부 변경해주는 함수
function HashColorOrg(){
	for(var i=0; i<HashTagList.length; i++){
		var Hash = HashTagList[i];
		var HashName = '#Hash_'+Hash;
		btname = HashName + '_bt'
		
		$(HashName).text( '' );
		$(btname).css('background-color', '#F7C2C2');
	}
	$('.WriteImgHide').css('display', 'none');
	document.getElementById("WriteImgOne").src = '';
	document.getElementById("WriteImgTwo").src = '';
	document.getElementById("WriteImgThree").src = '';
	$('.ImgNameList').text('');
}

// 이미지 업로드 시, 글쓰기 창에 미리보기
$('.ImgUpload_write').change(function(){
    var reader = new FileReader();
    reader.onload = function (e) {
		if( $('#WriteImgOne').attr('src') == '' ){
			document.getElementById("WriteImgOne").src = e.target.result;
			$('#imgDIVone').css('display', 'inline-block');
			//$('.ImgNameList').text( $('.ImgUpload_write').get(0).files[0].name );
			imgname_making();
			console.log('1');
		}
		else if ( $('#WriteImgTwo').attr('src') == '' ){
			document.getElementById("WriteImgTwo").src = e.target.result;
			$('#imgDIVtwo').css('display', 'inline-block');
			imgname_making();
			console.log('2');
		}
		else{
			document.getElementById("WriteImgThree").src = e.target.result;
			$('#imgDIVthree').css('display', 'inline-block');
			imgname_making();
		}
		
		
    };

    reader.readAsDataURL(this.files[0]);
});

// 글쓰기 이미지 파일 이름 문자열로 만들기
function imgname_making(){
	var filename=$('.ImgUpload_write').get(0).files[0].name;
	//console.log($('.ImgUpload_write').get(0).files);
	imgname = $('.ImgNameList').text();
	// ? 로 파일 구분
	$('.ImgNameList').text(imgname + filename+'?');
	
}

//  정렬 셀렉터 선택
/*
$('.PostSortSelect').change(function(){
	var select = $('.PostSortSelect').val();
	//alert($(this).val());
	// 마감임박순
	if(select == 'Deadline'){
		window.location.href = '/board/%&2$%1$@7&1D45^8E85';
	}
	// 가격 높은 순
	else if(select == 'HighCost'){
		window.location.href = '/board/%&2$%1$@7&1H45^8E85';
	}
	// 최신순
	else{
		window.location.replace('/board/%&2$%1$@7&1C45^8E85');
	}
});*/

$('.PostSortSelect').change(function(){
	var select = $('.PostSortSelect').val();
	$('.select_select').val(select);
	
});


$('.SearchByWhatButton').change(function(){
	var select = $('.SearchByWhatButton').val();
	
	$('.search_what_set').val(select);
	
});

//해쉬태그 누르면 색변하고 입력
$('.DesignerSpecialHash').click(function(){
	//$(this).css('background-color', '#FF4000');
	var hash_id =  $(this).text();
	console.log("3210");
	console.log(hash_id);
	console.log("321");
	var hash_set = $('.category_set').text();
	// 처음 클릭일 경우
	if(hash_set.indexOf(hash_id) == -1){
		$('.category_set').text(hash_set + hash_id);
		$(this).css('background-color', '#FF4000');
		console.log("first click");
	}
	else{ // 이미 클릭한 경우
		hash_set = hash_set.replace(hash_id, '');
		$(this).css('background-color', '#F7C2C2');
		$('.category_set').text(hash_set);
	}
	$('.category_set').val($('.category_set').text());
	
});

// 필터 껐다 켜기 
$('#Search_Filter').click(function(){
	var Box_OnOff = $('.FilterBoxOnOff').text();
	//필터 꺼져있을 경우
	if(Box_OnOff == ''){
		$('.FilterBox').css('display', 'block');
		$('.FilterBoxOnOff').text('on');
	}
	// 필터 켜져있을 경우
	else{
		$('.FilterBox').css('display', 'none');
		$('.FilterBoxOnOff').text('');
	}
});

function searching_start(){
	var search = $('#InputTextBox').val();
	$.ajax({
				url:'/searching_start',
				type: 'POST',
				dataType: 'json',
				data: {
					},
				
				success : function (data){
					$('#InputTextBox').val(search);
				}
		});
		$('#InputTextBox').val(search);
}

//이미지 누르면 해당 이미지 확대 함수
$('.ImgOne').click(function(){
	console.log('on');
	$('.img_show_one').attr('src', $(this).attr('src'));
	$('.img_big_box').css('display', 'block');
	//rgba로 그림자 색, 흐림 강도 설정
	$('.img_big_box').css('box-shadow', ' rgba(0,0,0,0.7) 0 0 0 9999px');
	$('.img_big_box').css('z-index', '100');
	// 위에는 박스 바깥 그림자, 아래는 박스 안쪽 그림자
	$('.show_img_box').css('box-shadow', 'inset rgba(0,0,0,0.7) 0 0 0 9999px');
});
//이미지 확대 후 화살표 누르면 사진 이동
$('.img_move').click(function(){
	if( $(this).attr('name') == 'img_left'){
		url = $(this).next().attr('src');
		src = url.split('/');
		result = $('#'+src[src.length-1].split('.')[0]).prev().attr('src');
	}else{
		url = $(this).prev().attr('src');
		src = url.split('/');
		result = $('#'+src[src.length-1].split('.')[0]).next().attr('src');
	}
	console.log(result);
	$('.img_show_one').attr('src', result);
});
//이미지 확대 끄기
$('.img_close').click(function(){
	$('.img_big_box').css('display', 'none');
});