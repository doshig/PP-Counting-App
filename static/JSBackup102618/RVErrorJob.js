(function(){
'use strict';

angular.module('RV.ErrorJob',[] )
	.controller('ErrorJobController',
		[ '$scope' , '$http', ErrorJobController]);
	
function ErrorJobController($scope, $http) {

	
	$scope.countdata = [];
	$http.get('/CountingLog/countlogs/').then(function(response){
		$scope.countdata = response.data;
		
	});
	


};
	

}());