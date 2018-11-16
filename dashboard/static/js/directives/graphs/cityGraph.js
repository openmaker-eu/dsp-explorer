export default function(){
    return{
            template:`
            <div class="entity-carousel__header short background-red text-white graph_title" ng-if="loading==false">
                 <h4>City Distribution</h4>
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
                latlong:"=",
                people:"="
            },
            controller: ['$scope', '$http', function($scope, $http){
                $scope.loading=true
                $scope.jobdata= {
                    city: 'London',
                    people:10
                }
                
                $scope.AskServer = function(){
                    var ads = $http.get('/api/v1.4/stats/city_distribution/')
                    ads.then(
                    function(success){
                        $scope.citydata = success.data;
                        $scope.loading=false;
                        $scope.colors=[],
                        $scope.data=[],
                        $scope.labels=[];
                        var i=0;
                            for (i = 0; i < $scope.citydata.length; i++) {
                                $scope.data.push($scope.citydata[i].people)
                                $scope.labels.push($scope.citydata[i].city)
                                $scope.colors.push({pointBackgroundColor:'#a8a6b5', backgroundColor:'rgba(80, 78, 94, 1)'})
                            }
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
                                console.log(tooltipItems)
                                return tooltipItems[0].xLabel +" people "
                                         },
                            label:function(){
                                return false
                            }
                        }
                
                    }
                
            }
           
            }]
        }
    }
