(function(){
'use strict';

angular.module('PP.DepartmentLog',[] )
	.controller('DepartmentLogController',
		[ '$scope' , '$http', DepartmentLogController]);
	
function DepartmentLogController($scope, $http) {
	
	document.getElementById("dep").focus();
	// Get the modal
	var modal = document.getElementById('validationModal');

	$scope.deptdata = [];
	$http.get('/DepartmentLog/deptlogs/').then(function(response){
		$scope.deptdata = response.data;
		
	});
	
	$scope.changeFocus = function () {
		
		document.getElementById("lotno").focus();
	
	};
	
	$scope.verifyFunction = function (deptid,deptlot) {
		
		var newdep = {
			Department: deptid,
			LotNo: deptlot,
		};
		
		$http.post('/DepartmentLog/deptlogs/',newdep)
			.then(function(response){
				$scope.wrongdep = response.data.WrongLocation;

				modal.style.display = "block";
				setTimeout(function() { modal.style.display = "none"; },3000);
				
				$scope.deptid = null;
				$scope.deptlot = null;
				document.getElementById("dep").focus();
				
			}, 
			function(){
				alert('Could not create Log');
			});

	};
	
	
	
};
	

}());