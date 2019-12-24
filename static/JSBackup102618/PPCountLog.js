(function(){
'use strict';

angular.module('PP.CountLog',[] )
	.controller('CountLogController',
		[ '$scope' , '$http', CountLogController]);
	
function CountLogController($scope, $http) {
	
	document.getElementById("employeid").focus();

	$scope.countdata = [];
	$http.get('/CountingLog/countlogs/').then(function(response){
		$scope.countdata = response.data;
		
	});
	
	$scope.passFocus = function () {
		
		document.getElementById("lotno").focus();
	
	};
	
	$scope.passFocus1 = function () {

		document.getElementById("nbpart").focus();
	
	};
	
	$scope.passFocus2 = function () {
		document.getElementById("btnvalidate").focus();

	};
	
	$scope.validateFunction = function (countemploye,countlot,countnbpart) {
		
		var newcount = {
			EmployeName: countemploye,
			LotNo: countlot,
			Quantity: countnbpart,
		};
		
		$http.post('/CountingLog/countlogs/',newcount)
			.then(function(response){
				$scope.actualid = response.data.id;
				$scope.actualjob = response.data.LotNo;
				$scope.movetoop = response.data.MoveTo;
				$scope.errorclockout = response.data.MissedClockOut;
				var supqty = response.data.SupposedQuantity;
				$scope.supquantitymax = supqty*1.055;
				$scope.supquantitymin = supqty*0.975;
				var prevcount = response.data.PreviousCount;
				$scope.allowedqty = response.data.ScrapAllowance ;
				$scope.prevcount = response.data.PreviousCount;

			},
			function(){
				alert('Could not create Count Log');
			});

	};
	
	$scope.resetFunction = function () {
		$scope.countemploye = null;
		$scope.countlot = null;
		$scope.countnbpart = null;
		$scope.actualid = null;
		$scope.actualjob = null;
		$scope.movetoop = null;
		$scope.errorclockout = null;
		$scope.supquantity = null;

	};
	
	
	
};
	

}());