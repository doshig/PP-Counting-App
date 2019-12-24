// Update 10/29/18 
//Add prevlotcount and prevmovetoop to record last lot and OP for display
// Add modal load and modal close funtionality to JS, remove from HTML
// add timeout delay to modal popup to correct display issues on mobile



//Update 11/2/18 - add hide element that links with count html update

//Update 2/22/19 - add Notes field for Jonathan M for hold area adding.

//Update 2/22/19 - Keep employee ID on count page 

//Update 2/25/19 - Add ng-change trigger on employee ID setItem
//Add items for OverrideQtys logic

//Update 04/11/19 - Add functions for Pipeline, end pipeline, add onload to load pipeline information into count page when end pipeline is pressed

//Update 04/12/19 - Work on adding ability to scan six jobs, then press button, to log all in at once for Jonathan Londono
// Update 04/16/ add update(data) function - does not exist yet

//Update 06/07/19 - Add data for lastcountdata to show last job counted in counting app
$(document).ready(function(){

    try{
        if($("div").hasClass("OnLoadCount")){
            	document.getElementById("employeid").focus();

            if(localStorage.getItem("employeeID")){
                document.getElementById("employeid").value = localStorage.getItem("employeeID");
                angular.element(document.getElementById("employeid")).triggerHandler('change'); //Calls ng-change, which then calls update() function
            }
            
            if(localStorage.getItem('completePipelineWO')){
                document.getElementById("lotno").value = localStorage.getItem("completePipelineWO");
                angular.element(document.getElementById("lotno")).triggerHandler('change'); //Calls ng-change, which then calls update() function
            //Set counting log WO 
            
            }
            if(localStorage.getItem('completePipelineCount')){
                document.getElementById("nbpart").value = localStorage.getItem("completePipelineCount");
                angular.element(document.getElementById("nbpart")).triggerHandler('change'); //Calls ng-change, which then calls update() function
            /// Set Count
            }
            if(localStorage.getItem('completePipelineBadge')){
                document.getElementById("employeid").value = localStorage.getItem("completePipelineBadge");
                angular.element(document.getElementById("employeid")).triggerHandler('change'); //Calls ng-change, which then calls update() function
            }
            if(localStorage.getItem('completePipelineBadge') && localStorage.getItem('completePipelineWO') && localStorage.getItem('completePipelineCount') ){
                document.getElementById("notes").value = "Pipeline Complete";
                angular.element(document.getElementById("notes")).triggerHandler('change'); //Calls ng-change, which then calls update() function            
            
            }
            
        }
    }
    catch(e){
        console.log(e);
    
    }
    finally{
        localStorage.setItem("employeeID", "");
        localStorage.setItem('completePipelineWO', "");
        localStorage.setItem('completePipelineCount', "");
    }
    
    try{
        if($("div").hasClass("OnLoadCountPipeline")){
            console.log("1");
            if(localStorage.getItem('passPipelineWO')){
                console.log("2");
                console.log("passPipelineWO here");
                document.getElementById("filterWOID").value = localStorage.getItem('passPipelineWO');
                angular.element(document.getElementById("filterWOID")).triggerHandler('change');
            
            }
            else{
                console.log("3");
                console.log('set filterWO blank');
                document.getElementById("filterWOID").value = "";
                console.log("filterWOID: ", document.getElementById("filterWOID").value);
                angular.element(document.getElementById("filterWOID")).triggerHandler('change');
            }
        }
    
    }
    catch(e){
        console.log("passpipelinewo error: ", e);
    
    }
    finally{
    
    }
    


});


//For testing the automatic update script
//E.G.  <script src="{% static 'PPCountLog.js' %}?1"></script> with ?1 makes browser re-get cachce
console.log("jelly");
console.log("peanut");


(function(){
'use strict';

angular.module('PP.CountLog',[] )
	.controller('CountLogController',
		[ '$scope' , '$http', CountLogController]).run(['$http', run]);
	
function CountLogController($scope, $http) {

    function ModifyString(arg) { 
       var result = arg ; // if not format we need, simply return the scanned data

       var matches  = arg.match("(?:[%][0-9]{1})([a-zA-Z0-9\-]{1,})([$][0-9]*)([$][sS]?[0-9]*)([$][0-9]*)([$][0-9]*)(?:[%]{1})"); 
 
       
       if(matches != null && matches.length > 0) // if the match was accepted
       {
                      result = "" ; 
                      for ( var i = 1 ; i < matches.length ; i ++)
                      {
                                     result +=  matches[i];  // concatenate matched strings literally as 123456$7$9$321
                      }
                      
                      var re = new RegExp("[$]", 'g'); // store new regex, which now does not have the /8 in it

                      result = result.replace(re, '/');  // replace the $ with /
       }
       
       return result ;

    }

	

	var prevjob;
	var prevmoveto;

	$scope.countdata = [];
	$http.get('/CountingLog/countlogs/').then(function(response){
		$scope.countdata = response.data;
		
		$scope.startid = $scope.countdata.id;
		
	});
	
	
	$scope.openpipelinedata = [];
	$http.get('/CountingLog/openpipelines/').then(function(response){
    	$scope.openpipelinedata = response.data;
	
	});	
	
	$scope.lastcountdata = [];
	$http.get('/CountingLog/lastcount/').then(function(response){
    	$scope.lastcountdata = response.data;
	
	});
	
	//All PassFocus iterations for countsix.html page
	$scope.countSixPassFocus = function(){
    	if(document.activeElement == document.getElementById('employeid')){
        	document.getElementById('lotno').focus();
    	}
    	else if(document.activeElement == document.getElementById('lotno')){
        	document.getElementById('nbpart').focus();
    	}
    	else if(document.activeElement == document.getElementById('nbpart')){
        	document.getElementById('notes').focus();
    	}
    	else if(document.activeElement == document.getElementById('notes')){
        	document.getElementById('lotno2').focus();
    	}    	
    	
    	else if(document.activeElement == document.getElementById('lotno2')){
        	document.getElementById('nbpart2').focus();
    	}    	
    	else if(document.activeElement == document.getElementById('nbpart2')){
        	document.getElementById('notes2').focus();
    	}    	
    	else if(document.activeElement == document.getElementById('notes2')){
        	document.getElementById('lotno3').focus();
    	}  
    	  	
    	else if(document.activeElement == document.getElementById('lotno3')){
        	document.getElementById('nbpart3').focus();
    	}
    	else if(document.activeElement == document.getElementById('nbpart3')){
        	document.getElementById('notes3').focus();
    	}
    	else if(document.activeElement == document.getElementById('notes3')){
        	document.getElementById('lotno4').focus();
    	}   
    	 	
    	else if(document.activeElement == document.getElementById('lotno4')){
        	document.getElementById('nbpart4').focus();
    	}    	
    	else if(document.activeElement == document.getElementById('nbpart4')){
        	document.getElementById('notes4').focus();
    	}    	
    	else if(document.activeElement == document.getElementById('notes4')){
        	document.getElementById('lotno5').focus();
    	}
    	
    	else if(document.activeElement == document.getElementById('lotno5')){
        	document.getElementById('nbpart5').focus();
    	}
    	else if(document.activeElement == document.getElementById('nbpart5')){
        	document.getElementById('notes5').focus();
    	}
    	else if(document.activeElement == document.getElementById('notes5')){
        	document.getElementById('lotno6').focus();
    	}    
    		
    	else if(document.activeElement == document.getElementById('lotno6')){
        	document.getElementById('nbpart6').focus();
    	}    	
    	else if(document.activeElement == document.getElementById('nbpart6')){
        	document.getElementById('notes6').focus();
    	}    	
    	else if(document.activeElement == document.getElementById('notes6')){
        	document.getElementById('createholdcount').focus();
    	}    	
    	
    	
    	
    	
    	
    }	
	
	$scope.passFocus = function () {
		document.getElementById("lotno").focus();

	};
	
	$scope.passFocus1 = function () {
		document.getElementById("nbpart").focus();
	
	};
	
	$scope.passFocus2 = function () {
		document.getElementById("btnvalidate").focus();

	};
	
	$scope.createPipeline = function(WO, opFrom, opTo){
    	console.log("here1");
    	
    	if(opFrom){
        	if(opFrom.length >= 2){
            	var leading2 = opFrom.slice(0,2)
            	if(leading2 == '%2'){
                	var transformOp = ModifyString(opFrom);
                	console.log(transformOp);
                	var splitStuff = transformOp.split("/");
                	console.log(splitStuff)
                	WO = splitStuff[0]+"/"+splitStuff[1]+"."+splitStuff[2];
                	opFrom = splitStuff[4];
                	//splitStuff[3] is the sub, not used
            	}
        	}
        }
    	if(opTo){
        	if(opTo.length >= 2){
            	var leading2 = opTo.slice(0,2)
            	if(leading2 == '%2'){
                	var transformOp = ModifyString(opTo);
                	console.log(transformOp);
                	var splitStuff = transformOp.split("/");
                	console.log(splitStuff)
                	WO = splitStuff[0]+"/"+splitStuff[1]+"."+splitStuff[2];
                	opTo = splitStuff[4];
                	//splitStuff[3] is the sub, not used
            	}
        	
        	}
    	}        	
    	if(WO && opFrom && opTo){
        	console.log("WO: ", WO);
        	console.log("opFrom: ", opFrom);
        	console.log("opTo: ", opTo);

        	var newPipeline = {
            	workOrder: WO,
            	opSequenceFrom: opFrom,
            	opSequenceTo: opTo
        	
        	};
        	
        	var url = '/CountingLog/pipelines/';
        	
        	$http.post(url, newPipeline)
        	.then(function(response){
            	localStorage.setItem('passPipelineWO', response.data.workOrder);
            	console.log("after post: ", response.data.workOrder);
            	location.reload();
        	
        	},
        	function(){
            	alert("Could not create pipeline");
         });
        	//save work order value to cache
        	//reload page 
        	//load cache value in
      }
    	else{
        	alert("Please fill in WO#, OpFrom, and OpTo fields");
    	}
    	console.log("here2");
    	//location.reload();
	
	}
	
	$scope.update = function(data){
    	var url = '/CountingLog/countlogs/'+data.id+'/';
    	$http.put(url, data);
	
	
	}
	
	
	$scope.updatePipeline = function(data){
    	var url = '/CountingLog/pipelines/' +data.id +'/';
    	$http.put(url, data).then(function(response){
        	$scope.totalCount = response.data.totalCount;
        	//console.log("dateCount1: ", response.data.dateCount1);
      console.log("put stuff done");    	
    	});
    	
    
    	
    	console.log("success");
    	localStorage.setItem('passPipelineWO', data.workOrder);
	
	}
	$scope.endPipeline = function(data){
    	console.log("data: ", data);
	    	var url = '/CountingLog/pipelines/' +data.id +'/';
	    	
	    	data.pipelineClosed = true;
	    	
    	$http.put(url, data).then(function(response){
        console.log("put stuff done");    	
    	});
    	console.log("success");
	   localStorage.setItem('completePipelineWO', data.workOrder);
	   if(data.totalCount){
    	   console.log("data.totalCount: ", data.totalCount);
    	   	   localStorage.setItem('completePipelineCount', data.totalCount);

	   }
	   else{
    	   console.log("$scope.totalCount: ", $scope.totalCount);
    	   	   localStorage.setItem('completePipelineCount', $scope.totalCount);

	   }
	   
	   if(data.buyOffBadge4 != 0){
    	   	   localStorage.setItem('completePipelineBadge', data.buyOffBadge4);

	   }
	   else if(data.buyOffBadge3 != 0){
	       	   	   localStorage.setItem('completePipelineBadge', data.buyOffBadge3);

	   }
	   else if(data.buyOffBadge2 != 0){
	       	   	   localStorage.setItem('completePipelineBadge', data.buyOffBadge2);

	   }
	   else if(data.buyOffBadge1 != 0){
	       	   	   localStorage.setItem('completePipelineBadge', data.buyOffBadge1);

	   }	   

    	//window.location.href = "CountingLog/count";
    	window.location.href = "/CountingLog/count/";
	}
	

	
	
	$scope.validateFunction = function (countemploye,countlot,countnbpart,notes) {
    	
    	if(countemploye == null){
        	countemployee = localStorage.getItem("employeeID");
    	
    	}
    	else{
        	console.log("countemploye: ", countemploye);
        	localStorage.setItem("employeeID", countemploye);
    	}
    	
    	
		//console.log("NOtes: ", notes);
		
		if(countemploye.length != 4){
    		alert('EMPLOYEE ID NOT 4 DIGITS');
    		$scope.resetFunction();
    		return;
		
		}
		// Reset and return if 
		if(countnbpart >100000){
    		alert('COUNT > 100,000 PARTS');
    		$scope.resetFunction();
    		return;
		
		}
		
		else{
            var newcount = {
    		  EmployeName: countemploye,
        		LotNo: countlot,
        		Quantity : countnbpart,
        		Notes : notes
        		

    		};

		}
		
		
				
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
				$scope.QLABOpen = response.data.QLabOpen;
				$scope.belowtarget = response.data.BelowTargetQty;
				$scope.desiredqty = response.data.DesiredQty;
				
				$scope.prevjob = $scope.actualjob;
				$scope.prevmoveto = $scope.movetoop;
				$scope.overrideqtys = response.data.OverrideQtys;
				

        	   document.getElementById("redfish").style.display = "none";
            	//document.getElementById("bluefish").style.display = "none";


			},
			function(){
				alert('Could not create Count Log');
			});
			//Give a short delay to modal to allow time for server response
        setTimeout(function(){
                    $("#nextOpModal").show();

        },500);

	};
	
	$scope.createNewCount = function(badge, lot, quantity, notes){
    	        var newcount = {
    		  EmployeName: badge,
        		LotNo: lot,
        		Quantity : quantity,
        		Notes : notes
        		

    		};
    	
    	return newcount;
	
	
	
	}
	
	
	$scope.createHoldCount = function(badgenum,countlot,countnbpart,notesToAdd,
                                	countlot2,countnbpart2,notesToAdd2,countlot3,
                                	countnbpart3,notesToAdd3,countlot4,countnbpart4,
                                	notesToAdd4,countlot5,countnbpart5,notesToAdd5,
                                	countlot6,countnbpart6,notesToAdd6){
        //At a minimum, badge and one lot need to be present to do a post
        
        var url = '/CountingLog/countlogs/';
                 	
        if(badgenum && countlot && countnbpart){
            // Proceed
            //If all 1 - do post
            
            var newCount = $scope.createNewCount(badgenum, countlot, countnbpart, notesToAdd);
            
            $http.post(url, newCount).then(function(response){
                //alert("Success1!");
                //$scope.actualid = response.data.id;
    				$scope.actualjob1 = response.data.LotNo;
    				$scope.movetoop1 = response.data.MoveTo;

            },
            function(e){
            console.log(e);
                alert("could not create hold2");
            
            });
            
            
            if(countlot2 && countnbpart2){
                var newCount = $scope.createNewCount(badgenum, countlot2, countnbpart2, notesToAdd2);

            
                $http.post(url, newCount).then(function(response){
                //alert("Success2!");
                //$scope.actualid2 = response.data.id;
    				$scope.actualjob2= response.data.LotNo;
    				$scope.movetoop2 = response.data.MoveTo;

                },
                function(e){
                    console.log(e);
                    alert("could not create hold2");
            
               });
            }
            if(countlot3 && countnbpart3){
            
                var newCount = $scope.createNewCount(badgenum, countlot3, countnbpart3, notesToAdd3);

            
                $http.post(url, newCount).then(function(response){
                //alert("Success3!");
                //$scope.actualid2 = response.data.id;
    				$scope.actualjob3= response.data.LotNo;
    				$scope.movetoop3 = response.data.MoveTo;

                },
                function(e){
                    console.log(e);
                    alert("could not create hold3");
            
               });            
            }
            if(countlot4 && countnbpart4){
                var newCount = $scope.createNewCount(badgenum, countlot4, countnbpart4, notesToAdd4);

            
                $http.post(url, newCount).then(function(response){
                //alert("Success4!");
                //$scope.actualid2 = response.data.id;
    				$scope.actualjob4= response.data.LotNo;
    				$scope.movetoop4 = response.data.MoveTo;

                },
                function(e){
                    console.log(e);
                    alert("could not create hold4");
            
               });  
                           }
            if(countlot5 && countnbpart5){
                var newCount = $scope.createNewCount(badgenum, countlot5, countnbpart5, notesToAdd5);

            
                $http.post(url, newCount).then(function(response){
                //alert("Success5!");
                //$scope.actualid2 = response.data.id;
    				$scope.actualjob5= response.data.LotNo;
    				$scope.movetoop5 = response.data.MoveTo;

                },
                function(e){
                    console.log(e);
                    alert("could not create hold5");
            
               });  
                           } 
            if(countlot6 && countnbpart6){
                var newCount = $scope.createNewCount(badgenum, countlot6, countnbpart6, notesToAdd6);

            
                $http.post(url, newCount).then(function(response){
                //alert("Success6!");
                //$scope.actualid2 = response.data.id;
    				$scope.actualjob6= response.data.LotNo;
    				$scope.movetoop6 = response.data.MoveTo;

                },
                function(e){
                    console.log(e);
                    alert("could not create hold6");
            
               });  
            }                       
        
            setTimeout(function(){
                $("#nextOpModal").show();

            },500);  
        
        
        }
        else{
            alert("Badge#, Lot#, parts required");
        
        }
                       	
	
	}
	
	
	
	$scope.resetFunction = function () { 	
        $("#nextOpModal").hide();
		//$scope.countemploye = null;
		$scope.countlot = null;
		$scope.countnbpart = null;
		$scope.actualid = null;
		$scope.actualjob = null;
		$scope.movetoop = null;
		$scope.errorclockout = null;
		$scope.supquantity = null;
		$scope.notesToAdd = null;
        
	};
	
	$scope.resetCountSixFunction = function(){
        $("#nextOpModal").hide();
        
        $scope.actualjob1 = null;
        $scope.actualjob2 = null;
        $scope.actualjob3 = null;
        $scope.actualjob4 = null;
        $scope.actualjob5 = null;
        $scope.actualjob6 = null;

        $scope.movetoop1 = null;
        $scope.movetoop2 = null;
        $scope.movetoop3 = null;
        $scope.movetoop4 = null;
        $scope.movetoop5 = null;
        $scope.movetoop6 = null;
        
		//$scope.countemploye = null;
		$scope.countlot = null;
		$scope.countlot2 = null;
		$scope.countlot3 = null;
		$scope.countlot4 = null;
		$scope.countlot5 = null;
		$scope.countlot6 = null;
		
		
		
		
		$scope.countnbpart = null;
		$scope.countnbpart2 = null;
		$scope.countnbpart3 = null;
		$scope.countnbpart4 = null;
		$scope.countnbpart5 = null;
		$scope.countnbpart6 = null;

    	$scope.notesToAdd = null;	
    	$scope.notesToAdd2 = null;	
    	$scope.notesToAdd3 = null;	
    	$scope.notesToAdd4 = null;	
    	$scope.notesToAdd5 = null;	
    	$scope.notesToAdd6 = null;	



		
		$scope.actualid = null;
		$scope.actualjob = null;
		$scope.movetoop = null;
		$scope.errorclockout = null;
		$scope.supquantity = null;
	}
	
	
	
};
	

}());

//This is needed for CSRF protection, see also .run(...) chain at top near .module
function run($http){
    $http.defaults.xsrfHeaderName = 'X-CSRFToken';
    $http.defaults.xsrfCookieName = 'csrftoken';

}
