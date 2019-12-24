(function(){
'use strict';

angular.module('LL.Labview',[] )
	.controller('LabviewController',
		[ '$scope' , '$http', LabviewController]);
	
function LabviewController($scope, $http) {
	
	$scope.labdata = [];
	$http.get('/LABLog/lablogs/').then(function(response){
		$scope.deptdata = response.data;
		
	});
	
	
	
};
	

}());