(function(){
'use strict';

angular.module('LL.Labcheck',[] )
	.controller('LabcheckController',
		[ '$scope' , '$http', LabcheckController]);
	
function LabcheckController($scope, $http) {
	
	document.getElementById("empid").focus();
	// Get the modal
	var modal = document.getElementById('validationModal');

	$scope.passFocusFunction = function() {
		document.getElementById("lotno").focus();
	};
	
	
	$scope.verifyFunction = function (empid,deptlot) {
		
		var newlablog = {
			EmployeName: empid,
			LotNo: deptlot,
			
		};
		
		$http.post('/LABLog/lablogs/',newlablog)
			.then(function(response){
				$scope.jobnotclosed = response.data.VisualNotClosed;

				modal.style.display = "block";
				$scope.deptlot = null;
				document.getElementById("empid").focus();
				
			}, 
			function(){
				alert('Could not create Log');
			});

	};
	
	
	
};
	

}());