(function(){
'use strict';

angular.module('RV.JobLocation',[] )
	.controller('JobLocationController',
		[ '$scope' , '$http', JobLocationController]);
	
function JobLocationController($scope, $http) {

	
	
	$scope.deptdata = [];
	$http.get('/DepartmentLog/deptlogs/').then(function(response){
		$scope.deptdata = response.data;
		
		
	});


};
	

}());