angular.module('JianzhiApp', ['ionic','JianzhiApp.config','JianzhiApp.services','JianzhiApp.directive','angularFileUpload'])

.config(function($stateProvider, $urlRouterProvider,$ionicConfigProvider) {
    // $ionicConfigProvider.tabs.position('bottom');

    $stateProvider
    //index
    .state(
        "index",{
            url:"",
            abstract:true,
            templateUrl:"pages/menu.html",
            controller:"menuCtrl"
        })
    .state(
        "index.jianzhi",
        {
            url:"/jianzhi",
            views:{
                "jianzhi":{
                    templateUrl:"pages/jianzhi.html",
                    controller:"jianzhiCtrl"
                }
            }
        })
    .state(
        "index.jiajiao",
        {
            url:"/jiajiao",
            views:{
                "jiajiao":{
                    templateUrl:"pages/jiajiao.html",
                    controller:"MyYCtrl"
                }
            }
        })
    //login
    .state(
        "login",{
            url:"/login",
            templateUrl:"pages/login.html",
            controller:"LoginCtrl"
        })
    //register
    .state(
        "register",{
            url:"/register",
            templateUrl:"pages/register.html",
            controller:"RegCtrl"
        })
    //info
    .state(
        "info",{
            url:"/info",
            templateUrl:"pages/info.html",
            controller:"infoCtrl"
        })
    //我的兼职
    .state(
        "myjianzhi",{
            url:"/myjianzhi",
            templateUrl:"pages/myjianzhi.html",
            controller:"MyCtrl"
        })
    .state(
        "fileupload",{
            url:"/upload",
            templateUrl:"pages/upload.html",
            controller:"uploadCtrl"
        })
    $urlRouterProvider.otherwise('/jianzhi');
})

.controller('MyYCtrl', ['$scope', 'FileUploader','ENV','callApi','User', function($scope, FileUploader,ENV,callApi,User) {
    
}])
;