export default function(){
    return{
            template:`
            <div class="entity-carousel__header short background-red text-white">
                 <h4>Age Distribution</h4>
            </div>
            <br>
            <div class="block-square" ng-if="loading==false">
                <div style="background:#ff0;">
                    <canvas class="chart chart-bar" style="width:100%; height:100%;"
                        chart-data="data" chart-labels="labels" chart-options="options" chart-colors="colors">
                    </canvas>    
                </div>
            </div>
             `,
            transclude:true,
            scope:{
                zero_to_thirty:"=",
                thirty_to_forty:"=",
                forty_to_fifty:"=",
                over_fifty:"="      
            },
            controller: function($scope, $http){
                $scope.loading=true
                $scope.agedata= {
                    zero_to_thirty: 10,
                    thirty_to_forty: 5,
                    forty_to_fifty: 1,
                    over_fifty:3
                }
                
                $scope.AskServer = function(){
                    var ads = $http.get('/api/v1.4/stats/age_distribution/')
                    ads.then(
                    function(success){ 
                        $scope.agedata = success.data; 
                        $scope.loading=false
                        console.log('fhjfjkyry')
                        console.log($scope.agedata.zero_to_thirty)
                        $scope.loading=false
                        $scope.data=[$scope.agedata.zero_to_thirty, $scope.agedata.thirty_to_forty, $scope.agedata.forty_to_fifty, $scope.agedata.over_fifty]
                        },
                    function(error){ console.log("ritenta");$scope.loading=false
                        }
                    )
                }
                $scope.AskServer();
                
                
                $scope.labels= ['0-30', '30-40', '40-50', '50+'];
                $scope.colors= ['#a8a6b5','#a8a6b5','#a8a6b5','#a8a6b5']
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
                            scaleLabel:{
                                display: true,
                                labelString:'Age Intervals'
                            }
                        }],
                    },
                        
                    tooltips: {
                            callbacks: {
                                title:function(tooltipItems) {
                                    console.log(tooltipItems)
                                    return tooltipItems[0].yLabel +" people "
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