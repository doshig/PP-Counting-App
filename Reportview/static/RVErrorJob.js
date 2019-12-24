//10/23/18 Update to auto populate date field to sort

//1/18/19 Update to auto populate date field to sort, was missing.

(function(){
'use strict';

angular.module('RV.ErrorJob',[] )
	.controller('ErrorJobController',
		[ '$scope' , '$http', ErrorJobController]).run(['$http',run]);
	
function ErrorJobController($scope, $http) {
    
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
	
	
	
	
	
	$scope.countdata = [];
	$http.get('/CountingLog/countlogs/').then(function(response){
		$scope.countdata = response.data;
		
	});
	
		$scope.pipelinedata = [];
	$http.get('/CountingLog/pipelines/').then(function(response){
    	$scope.pipelinedata = response.data;
	
	
	});
	
	$scope.update = function(data){
    	var url = '/CountingLog/countlogs/'+data.id+'/';
    	$http.put(url, data);
	
	
	}
	
	
};


	

}());
//This is needed for CSRF protection, see also .run(...) chain at top near .module
function run($http){
    $http.defaults.xsrfHeaderName = 'X-CSRFToken';
    $http.defaults.xsrfCookieName = 'csrftoken';

}

