(function(){
'use strict';

angular.module('RV.JobLocation',[] )
	.controller('JobLocationController',
		[ '$scope' , '$http', JobLocationController]);
	
function JobLocationController($scope, $http) {
    var n =  new Date();
    var y = n.getFullYear();
    var m = n.getMonth() + 1;
    var d = n.getDate() ;
        
    m = '0' + m;
    m = m.slice(-2);
    
    d = '0'+d
    d = d.slice(-2)
    $scope.pizza = (y + "-" + m + "-" + d);
  
    $scope.filterdate = $scope.pizza;
	
	
	$scope.deptdata = [];
	$http.get('/DepartmentLog/deptlogs/').then(function(response){
		$scope.deptdata = response.data;
		
		
	});


};
	

}());