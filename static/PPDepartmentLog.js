
// Added ability to log up to six department jobs at once for hold area
// added CSRF protection

// 04/16/19 Fix verify function to work with new departmentloguser model
//08/xx/19 - add note logic to same from deptlog
//08/23/19 - add noteid = null on reset 
(function(){
'use strict';

angular.module('PP.DepartmentLog',[] )
	.controller('DepartmentLogController',
		[ '$scope' , '$http', DepartmentLogController]).run(['$http', run]);
	
function DepartmentLogController($scope, $http) {
	
	document.getElementById("dep").focus();
	// Get the modal
	var modal = document.getElementById('validationModal');

	$scope.deptdata = [];
	$http.get('/DepartmentLog/deptlogs/').then(function(response){
		$scope.deptdata = response.data;
		
	});
	
	$scope.deptlogusers = [];
	$http.get('/DepartmentLog/deptlogusers/').then(function(response){
    	$scope.deptlogusers = response.data;
    	
	
	})
	
	$scope.changeFocus = function () {
		
		document.getElementById("lotno").focus();
	
	};
	$scope.changeFocus2 = function () {
		
		document.getElementById("dep").focus();
	
	};	
	//deliberate that 2 and 3 go to same id
	$scope.changeFocus3 = function () {
		console.log("working");
		document.getElementById("dep").focus();
	
	};		
	
	
	
	$scope.verifyFunction = function (deptid,deptlot,departmentloguser, note) {
	
    	var empname = departmentloguser.listNumber + " - " + departmentloguser.userName;
	
		var url = '/DepartmentLog/deptlogs/';
		
		console.log("deptid: ", deptid);
		console.log("deptlot: ", deptlot);
		console.log("empname: ", empname);
		
		
		var newdep = {
			EmployeName: empname,
			Department: deptid.toUpperCase(),
			LotNo: deptlot,
			Notes: note
		};
		
		$http.post(url,newdep)
			.then(function(response){
				$scope.wrongdep = response.data.WrongLocation;

				$scope.correctdept = response.data.CorrectDept;
				$scope.altdept = response.data.AllowedDepts;	
							//modal.style.display = "block";
				//setTimeout(function() { modal.style.display = "none"; },3000);
				
				$scope.deptid = null;
				$scope.deptlot = null;
				document.getElementById("dep").focus();

				
			}, 
			function(){
				$scope.deptid = null;
				$scope.deptlot = null;
				$scope.deptid = "";
				$scope.deptlot = "";
				$scope.noteid = null;
				$scope.noteid = "";
				alert('Could not create Log');

			});
			setTimeout(function(){
    			$("#validationModal").show();
			}, 1000);

	};
	
	$scope.createDeptSix = function(departmentloguser, deptid, deptlot, deptlot2, deptlot3, deptlot4, deptlot5, deptlot6 ){
		var url = '/DepartmentLog/deptlogs/';
		var employee = departmentloguser.listNumber + " - " + departmentloguser.userName;
		console.log("employee: ", employee);
		console.log("deptid: ", deptid);
		console.log("deptlot: ", deptlot);
		console.log("hello");

    	if(employee && deptid && deptlot){
    	
        	var newdep1 = {
            	EmployeName: employee,
            	Department: deptid.toUpperCase(),
            	LotNo: deptlot,
        	};
        	
        	$http.post(url, newdep1).then(function(response){
            	console.log("newdep1 success.");
            	$scope.wrongdep1 = response.data.WrongLocation;
				$scope.correctdept1 = response.data.CorrectDept;
				$scope.altdept1 = response.data.AllowedDepts;
        	
        	}),
        	function(e){
            	console.log(e);
            	alert("Could not create deptsix 1");
        	}
        	
        	if(deptlot2){
            	var newdep2 = {
                	EmployeName: employee,
                	Department: deptid.toUpperCase(),
                	LotNo: deptlot2,
            	};  
            	
            	$http.post(url, newdep2).then(function(response){
            	console.log("newdep2 success.");
            	$scope.wrongdep2 = response.data.WrongLocation;
				$scope.correctdept2 = response.data.CorrectDept;
				$scope.altdept2 = response.data.AllowedDepts;
            	},
            	function(e){
                	console.log(e);
                	alert("could not create deptsix 2");
            	});
        	}
        	if(deptlot3){
            	var newdep3 = {
                	EmployeName: employee,
                	Department: deptid.toUpperCase(),
                	LotNo: deptlot3,
            	};  
            	
            	$http.post(url, newdep3).then(function(response){
            	console.log("newdep3 success.");
                	$scope.wrongdep3 = response.data.WrongLocation;
    				$scope.correctdept3 = response.data.CorrectDept;
    				$scope.altdept3 = response.data.AllowedDepts;            	

            	},
            	function(e){
                	console.log(e);
                	alert("could not create deptsix 3");
            	});
        	}  
        	
	       if(deptlot4){
            	var newdep4 = {
                	EmployeName: employee,
                	Department: deptid.toUpperCase(),
                	LotNo: deptlot4,
            	};  
            	
            	$http.post(url, newdep4).then(function(response){
            	console.log("newdep4 success.");
                	$scope.wrongdep4 = response.data.WrongLocation;
    				$scope.correctdept4 = response.data.CorrectDept;
    				$scope.altdept4 = response.data.AllowedDepts;
            	},
            	function(e){
                	console.log(e);
                	alert("could not create deptsix 4");
            	});
        	}
        	
        	if(deptlot5){
            	var newdep5 = {
                	EmployeName: employee,
                	Department: deptid.toUpperCase(),
                	LotNo: deptlot5,
            	};  
            	
            	$http.post(url, newdep5).then(function(response){
            	            	console.log("newdep5 success.");
                	$scope.wrongdep5 = response.data.WrongLocation;
    				$scope.correctdept5 = response.data.CorrectDept;
    				$scope.altdept5 = response.data.AllowedDepts;
            	},
            	function(e){
                	console.log(e);
                	alert("could not create deptsix 5");
            	});
        	}
        	if(deptlot6){
            	var newdep6 = {
                	EmployeName: employee,
                	Department: deptid.toUpperCase(),
                	LotNo: deptlot6,
            	};  
            	
            	$http.post(url, newdep6).then(function(response){
    	          console.log("newdep6 success.");
                $scope.wrongdep6 = response.data.WrongLocation;
    				$scope.correctdept6 = response.data.CorrectDept;
    				$scope.altdept6 = response.data.AllowedDepts;

            	},
            	function(e){
                	console.log(e);
                	alert("could not create deptsix 6");
            	});
        	}        	        	
        	
        		setTimeout(function(){
    			$("#validationModal").show();
			}, 1000);
        	
    	
    	
    	}
    	else{
        	alert("Employee, Dept, or WorkOrder1 missing!");
    	}
	
	
	}
	
	$scope.resetFunction = function(){
    	$("#validationModal").hide();
			$scope.deptid = null;
			$scope.deptlot = null;
			document.getElementById("dep").focus();

					
	};
	
	$scope.resetDeptSix = function(){
    	$("#validationModal").hide();
			$scope.deptid = null;
			$scope.deptlot = null;
			$scope.deptlot2 = null;
			$scope.deptlot3 = null;
			$scope.deptlot4 = null;
			$scope.deptlot5 = null;
			$scope.deptlot6 = null;
	
		document.getElementById("dep").focus();

	}
	
	$scope.changeFocusDeptSix = function(){
	//Pass from Department to Wo1, work order 2...6, create hold department button
    //console.log("enter1");
	
    	if(document.activeElement == document.getElementById('dep')){
        	document.getElementById('lotno').focus();
    	}
    	else if(document.activeElement == document.getElementById('lotno')){
        	document.getElementById('lotno2').focus();
    	}
    	else if(document.activeElement == document.getElementById('lotno2')){
        	document.getElementById('lotno3').focus();
    	}
    	else if(document.activeElement == document.getElementById('lotno3')){
        	document.getElementById('lotno4').focus();
    	}
    	else if(document.activeElement == document.getElementById('lotno4')){
        	document.getElementById('lotno5').focus();
    	}
    	else if(document.activeElement == document.getElementById('lotno5')){
        	document.getElementById('lotno6').focus();
    	}
    	else if(document.activeElement == document.getElementById('lotno6')){
        	document.getElementById('createdeptmentlogsix').focus();
    	}					

	
	}
	
	
	
};
	

}());

function run($http){
    $http.defaults.xsrfHeaderName = 'X-CSRFToken';
    $http.defaults.xsrfCookieName = 'csrftoken';

}
