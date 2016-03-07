angular.module('JianzhiApp')

.controller('jianzhiCtrl', ['$scope','$ionicPopup','$log','$rootScope','callApi','User','MessageShow','$ionicScrollDelegate','$state', function($scope,$ionicPopup,$log,$rootScope,callApi,User,MessageShow,$ionicScrollDelegate,$state){
	var user = User.getCurrentUser();
	var pagenumber = 1;
	var pagesize=5;
	var scrollState=true;
	var enroll = function(item){
			if(!User.judgeUser()){
				if(User.getInfoState()){
						var confirmPopup = $ionicPopup.show({
			               cssClass:'enroll_popup',
			               title: '提示',
			               scope:$scope,
			               buttons:[
			               		{
			               			text:'取消',
			               			type:'button-clear',
			               			onTap:function(e){
			               				console.log("cancle");
			               			}
			               		},
			               		{
			               			text:'确定',
			               			type:'button-clear',
			               			onTap:function(e){
			               				newOrder(item);
			               			}
			               		}
			               ],
			               template: '<p>确定报名该兼职？</p><p>(报名成功后我们会通过QQ，电话等方式联系你。请等候通知)</p>'
			             });
					} else {
						MessageShow.MessageShow("请先完善资料",1000);
						$state.go("info");
					}
			} else {
				MessageShow.MessageShow("请先登录",1000);
				$state.go("login");
			}
	};

	var jianzhi_info = []
	var getList = function(pagenumber,callback,type){
		var token = user.token||null;
		callApi.getData("/item/list","POST",{"pagenumber":pagenumber,"pagesize":pagesize},token)
			.then(function(response){
				if(response.code==200){
					dealdata(response.content);
					$scope.no_content=false;
					if(response.content.length<pagesize){
						$scope.scrollState=false;
						if(response.content.length==0&&pagenumber==1){
							$scope.no_content=true;
						}
					}
					if(type==1){
						$scope.jianzhi_info = $scope.jianzhi_info.concat(response.content);
						if(response.content.length<pagesize){
							MessageShow.MessageShow("没有更多数据",1000);
						}
					} else if(type==0){
						$scope.jianzhi_info = response.content;
						if(response.content.length<1){
							MessageShow.MessageShow("暂时没有兼职",1000);
						}
					} else {
						$scope.jianzhi_info = response.content;
						MessageShow.MessageShow("刷新成功",1000);
						if(response.content.length<1){
							MessageShow.MessageShow("没有更多数据",1000);
						}
					}
					
				} else {
					MessageShow.MessageShow(response.content,1000);
				}
				callback();
			}, function(error){
				MessageShow.MessageShow("网络错误",2000);
				$scope.scrollState=false;
				callback();
			})
	}

	var dealdata = function(data){
		for(var i=0;i<data.length;i++){
			var start = data[i].start_time.split('-');
			var end = data[i].end_time.split('-');
			data[i].time = start[1]+"."+start[2]+"-"+end[1]+"."+end[2]+" "+start[0];
			data[i].state = {'9':true,'8':false}[data[i].state];
		}
	}
	$scope.addItems = function(){
		pagenumber+=1;
		setTimeout(function(){
			getList(pagenumber,function(){
				$scope.$broadcast('scroll.infiniteScrollComplete');
			},1);
		},1000);
	}

	$scope.doRefresh = function(){
		console.log("refresh");
		pagenumber = 1;
		$scope.scrollState=true;
		getList(pagenumber,function(){
			$scope.$broadcast("scroll.refreshComplete");
		},2);
	}

	var newOrder = function(item){
		item.state=false;
		callApi.getData("/record/new","POST",{"iid":item.iid},user.token)
			.then(function(response){
				if(response.code==200){
					MessageShow.MessageShow("报名成功",1000);
				} else {
					MessageShow.MessageShow(response.content,1000);
					item.state=true;
				}
			}, function(error){
				item.state=true;
				MessageShow.MessageShow("网络错误",2000);
			});
	}
	
	function init(){
		getList(pagenumber,function(){
		},0);

	};
	$scope.jianzhi_info = jianzhi_info;
	$scope.enroll = enroll;
	$scope.scrollState = scrollState;
	init();
}])

//我的兼职页面
.controller('MyCtrl', ['$scope','$ionicPopup','$log','callApi','User','MessageShow','$ionicScrollDelegate','$state', function($scope,$ionicPopup,$log,callApi,User,MessageShow,$ionicScrollDelegate,$state){
	var user = User.getCurrentUser();
	var pagenumber = 1;
	var scrollState=true;
	var jianzhi_info={};
	var pagesize=5;

	var enroll = function(item){

		if(!User.judgeUser()){
             var confirmPopup = $ionicPopup.show({
               cssClass:'enroll_popup',
               title: '提示',
               scope:$scope,
               buttons:[
               		{
               			text:'取消',
               			type:'button-clear',
               			onTap:function(e){
               				
               			}
               		},
               		{
               			text:'确定',
               			type:'button-clear',
               			onTap:function(e){
               				CancleOrder(item);
               			}
               		}
               ],
               template: '<p>确定取消报名该兼职?</p>'
             });
        } else {
        	MessageShow.MessageShow("请先登录",1000);
			$state.go("login");
        }
             
	};


	var getList = function(pagenumber,callback,type){
		var token = user.token||null;
		if(User.judgeUser()){
			MessageShow.MessageShow("请先登录",1000);
			$state.go("login");
		} else {
			callApi.getData("/item/mylist","POST",{"pagenumber":pagenumber,"pagesize":pagesize},token)
				.then(function(response){
					if(response.code==200){
						dealdata(response.content);
						$scope.no_content=false;
						if(response.content.length<pagesize){
							$scope.scrollState=false;
							if(response.content.length==0&&pagenumber==1){
								$scope.no_content=true;
							}
						}
						if(type==1){
							$scope.jianzhi_info = $scope.jianzhi_info.concat(response.content);
							if(response.content.length<pagesize){
								MessageShow.MessageShow("没有更多数据",1000);
							}
						} else if(type==0){
							$scope.jianzhi_info = response.content;
							if(response.content.length<1){//没有兼职
								MessageShow.MessageShow("暂时没有兼职",1000);
							}
						} else {
							$scope.jianzhi_info = response.content;
							if(response.content.length==pagesize){
								$scope.scrollState=true;
							}
							MessageShow.MessageShow("刷新成功",1000);
						}
						
					} else {
						MessageShow.MessageShow(response.content,1000);
					}
					callback();
				}, function(error){
					MessageShow.MessageShow("网络错误",2000);
					$scope.scrollState=false;
					callback();
				})
			}
	}

	var dealdata = function(data){
		for(var i=0;i<data.length;i++){
			var start = data[i].start_time.split('-');
			var end = data[i].end_time.split('-');
			data[i].time = start[1]+"."+start[2]+"-"+end[1]+"."+end[2]+" "+start[0];
			data[i].mystate = {'3':"取消",'1':"已拒绝",'2':"成功"}[data[i].state];
			data[i].state = {'3':true,'1':false,'2':false}[data[i].state];
		}
	}
	$scope.addItems = function(){
		pagenumber+=1;
		getList(pagenumber,function(){
			$scope.$broadcast('scroll.infiniteScrollComplete');
		},1000);
	}

	$scope.doRefresh = function(){
		pagenumber = 1;
		getList(pagenumber,function(){
			$scope.$broadcast("scroll.refreshComplete");
		},2);
	}

	var CancleOrder = function(item){
			item.state=false;
			callApi.getData("/record/delete","POST",{"rid":item.rid},user.token)
				.then(function(response){
					if(response.code==200){
						MessageShow.MessageShow("退出报名成功",1000);
					} else {
						MessageShow.MessageShow(response.content,1000);
					}
				}, function(error){
					MessageShow.MessageShow("网络错误",2000);
				});
	}
	
	function init(){
		getList(pagenumber,function(){
		},0);

	};
	$scope.jianzhi_info = jianzhi_info;
	$scope.enroll = enroll;
	$scope.scrollState = scrollState;
	init();

}])

//个人信息页面
.controller('infoCtrl', ['$scope','User','MessageShow','callApi','$state','EventService','$rootScope', function($scope,User,MessageShow,callApi,$state,EventService,$rootScope){
	console.log("start");
	var user = User.getCurrentUser();
	var toggle_group = {
		'one':false,
		'two':false,
		'three':false
	}
	var info = {
		'course':'',
		'experience':'',
		'intention':'',
		'name':'',
		'qq':'',
		'phone':'',
		'cardnum':''
	}
	var info_toggle = function(number){
		toggle_group[number] = !toggle_group[number];
	};

	var check_info = function(){
		var out_consider = ['experience','intention'];
		for(i in info){
			if (out_consider.indexOf(i)==-1){
				if(!info[i]||info[i].length<1){
					return "基础信息不能为空";
				}
			}
		}
		return null;
	}
	var update_info = function(){
		var error = check_info();
		if(error){
			$scope.error_message =error;
		} else {
			callApi.getData("/info/update","POST",info,user.token)
				.then(function(response){
					if(response.code!=200){
	                    MessageShow.MessageShow(response.content,2000);
	                } else {
	                	EventService.broadcast("update");
	                    MessageShow.MessageShow("修改成功",1000);
	                    setTimeout(function(){
	                    	$state.go("index.jianzhi");
	                    },1000);
	                }
				},function(error){
					MessageShow.MessageShow("网络错误",2000);
				})
			}
	}

	$scope.show_group = toggle_group
    $scope.info_toggle = info_toggle;
    $scope.info = info;
    $scope.update = update_info;
    var get_info = function() {
    	callApi.getData('/info/get','POST',null,User.getCurrentUser().token)
				.then(function(response){
					if(response.code==200){
						for(i in info){
							info[i] = response.content[i];
						}
					} else {
						MessageShow.MessageShow(response.content,1000);
					}
				}, function(error){
					MessageShow.MessageShow("网络错误",1000);
				})
    }
    $rootScope.$on("update",function(){
			get_info();
		});
    function init (argument) {
    	if(User.judgeUser()){
    		MessageShow.MessageShow("请先登录",1000);
    		$state.go("login");
    	} else {
    		get_info();
    	}
    }
    init();
}])

//菜单也控制器
.controller('menuCtrl', ['$scope','User','MessageShow','$log','$rootScope','$state','callApi', function($scope,User,MessageShow,$log,$rootScope,$state,callApi){
	var user = User.getCurrentUser();
	var picture_base = "./static/img/";
	var info = {
		'username':"未登录",
		'url':'./static/img/index/tou.jpg',
		'state':!User.judgeUser()
	}
	var getUserName = function() {
		// get_picture_click();
		if(!User.judgeUser()){
			callApi.getData('/info/get','POST',null,User.getCurrentUser().token)
				.then(function(response){
					if(response.code==200){
						User.setInfoState(response.content);
						$scope.info.username = response.content.name;
						$scope.info.state=true;
						if(response.content.picture&&response.content.picture.length>1){
							$scope.info.url = picture_base+response.content.picture;
						}
					} else {
						// MessageShow.MessageShow(response.content,1000);
					}
				}, function(error){
					MessageShow.MessageShow("网络错误",1000);
				})
		} else {
			$scope.info = {
				'username':"未登录",
				'url':'./static/img/index/tou.jpg',
				'state':!User.judgeUser()
			};
		}
	}
	function init(){
		getUserName();
		
	}

	$scope.logout = function(){
		User.logout();
		getUserName();
	}

	var get_picture_click = function(){
		if(User.judgeUser()){
			$state.go("login");
		} else {
			$state.go("index.jianzhi");
		}
	}
	$scope.get_picture_click = get_picture_click;
	$rootScope.$on("update",function(){
			getUserName();
		});
	init();
	$scope.info = info;
}])
//登录页控制器
.controller('LoginCtrl', ['User','$scope','$log','MessageShow','$state','$stateParams','EventService',
		function(User,$scope,$log,MessageShow,$state,$stateParams,EventService){
	$scope.formData = {
		'login_username':'',
		'login_password':''
	};
	var laststate = "index.jianzhi";

	var check_dormData = function(formData){
		if(formData.login_username.length < 1){
			return "用户名不能为空!";
		} else if(formData.login_password.length < 1){
			return "密码不能为空";
		} else {
			return null;
		}
	}

	var login = function(){
		
		var error = check_dormData($scope.formData);
		if(error){
			$scope.error_message = error;
		} else {
			User.login($scope.formData.login_username,$scope.formData.login_password)
				.then(function(response){
					$log.debug(response)
					if(response){
						$scope.error_message = response;
					} else {
						MessageShow.MessageShow("登录成功",1000);
						EventService.broadcast("update");
						$state.transitionTo(laststate, {},{reload: true, notify:true});
						
					}

				},function(error){
					MessageShow.MessageShow("网络错误",1000);
				})
		}
	}
	$scope.login = login;
}])

//注册页控制器
.controller('RegCtrl', ['$scope','User','$log','MessageShow','$state','EventService',
		function($scope,User,$log,MessageShow,$state,EventService){
	var laststate = "info";
	$scope.formData = {
		'reg_username':'',
		'pwd':'',
	};
	var check_dormData = function(formData){
		if(formData.reg_username.length < 1){
			return "用户名不能为空!";
		} else if(formData.pwd.length < 1){
			return "密码不能为空";
		} else {
			return null;
		}
	};

	$scope.register = function(isvalid){
		var error = check_dormData($scope.formData);
		if(error){
			$scope.error_message = error;
		} else {
			User.register($scope.formData.reg_username,$scope.formData.pwd)
				.then(function(response){
					$log.debug(response)
					if(response){
						$scope.error_message = response;
					} else {
						MessageShow.MessageShow("注册成功",1000);
						EventService.broadcast("update");
						setTimeout(function(){
							$state.transitionTo(laststate, {},{reload: true, notify:true});
						},1000)
					}

				},function(error){
					MessageShow.MessageShow("网络错误",1000);
				})
		}
	}
}])

//上传图片
.controller('uploadCtrl', ['$scope', 'FileUploader','ENV','callApi','User', function($scope, FileUploader,ENV,callApi,User) {
    var uploader = $scope.uploader = new FileUploader({
        url: ENV.api+"/upload"
    });

    // FILTERS

    uploader.filters.push({
        name: 'imageFilter',
        fn: function(item /*{File|FileLikeObject}*/, options) {
            var type = '|' + item.type.slice(item.type.lastIndexOf('/') + 1) + '|';
            return '|jpg|png|jpeg|bmp|gif|'.indexOf(type) !== -1;
        }
    });

    uploader.onCompleteItem = function(fileItem, response, status, headers) {
        callApi.getData('/info/picture',"POST",{'picture':response.path},User.getCurrentUser().token)
            .then(function(response){
                console.log(response);
            }, function(error){

            });
    };
    uploader.onCompleteAll = function() {
        console.info('onCompleteAll');
    };
}])

;
