export default function(){
    return{
            template:`
            <div class="entity-carousel__header short background-red text-white graph_title" ng-if="loading==false">
                 <h4>Job Distribution</h4>
            </div>
            <br>
            <div class="block-rectangular" ng-if="loading==false">
                <div>
                    <canvas class="chart chart-horizontalBar" style="width:100%; height:100%;"
                        chart-data="data" chart-labels="labels" chart-options="options" chart-colors="colors">
                    </canvas>    
                </div>
            </div>
             `,
            transclude:true,
            scope:{
                occupation:"=",
                people:"="
            },
            controller: function($scope, $http){
                $scope.loading=true 
                $scope.jobdata= {
                    occupation: 'designer',
                    people:10
                }              
                
                $scope.AskServer = function(){
                    var ads = $http.get('/api/v1.4/stats/job_distribution/')
                    ads.then(
                    function(success){ 
                        $scope.jobdata = success.data; 
                        $scope.loading=false;
                        $scope.colors=[],                       
                        $scope.data=[],
                        $scope.labels=[];
                        var i=0;
                            for (i = 0; i < $scope.jobdata.length; i++) { 
                                $scope.data.push($scope.jobdata[i].people)
                                $scope.labels.push($scope.jobdata[i].occupation) 
                                $scope.colors.push({pointBackgroundColor:'#a8a6b5', backgroundColor:'rgba(80, 78, 94, 1)'})                            }
                           
                        },
                    function(error){ console.log("ritenta");$scope.loading=false
                        }
                    )
                }
                $scope.AskServer();
                
                
               
                
                $scope.options = {
                    animation: false,
                    responsive: true,
                    aspectRatio:1,
                    mantainAspectRatio: true,
                    legend: {
                        display:false,
                        position: 'bottom',
                           
                      },
                    scales: {
                        xAxes:[{
                            barPercentage: 0.8,
                            ticks:{
                                beginAtZero: true
                            },          
                            scaleLabel:{
                                display: true,
                                labelString:''
                            }
                        }],
                    },
                        
                    tooltips: {
                        callbacks: {
                            title:function(tooltipItems) {
                                return tooltipItems[0].xLabel +" people "
                                         },  
                            label:function(){
                                return false
                            }    
                        }
                
                    }
           
                }
            }
        }
    }