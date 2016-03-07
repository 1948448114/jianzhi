angular.module('JianzhiApp', ['ionic','JianzhiApp.config','JianzhiApp.services'])

.config(function($stateProvider, $urlRouterProvider,$ionicConfigProvider) {
    // $ionicConfigProvider.tabs.position('bottom');

    $stateProvider
//管理员
    .state(
        "admin",{
            url:"/admin",
            abstract:true,
            templateUrl:"pages/menu.html",
            controller:"MyYCtrl"
        })
    .state(
        "admin.jianzhi",
        {
            url:"/jianzhi",
            views:{
                "adminjianzhi":{
                    templateUrl:"pages/jianzhi.html",
                    controller:"AdminjianzhiCtrl"
                }
            }
        })
    .state(
        "admin.new",
        {
            url:"/new",
            views:{
                "new":{
                    templateUrl:"pages/new.html",
                    controller:"NewCtrl"
                }
            }
        })
    .state(
        "adminLogin",{
            url:"/login",
            templateUrl:"pages/login.html",
            controller:"adminLoginCtrl"
        })
    ;
    $urlRouterProvider.otherwise('/admin/jianzhi');
})
.controller('MyYCtrl', function($scope,$state) {
     $scope.search = function(){
        console.log("search");
     }
})
;