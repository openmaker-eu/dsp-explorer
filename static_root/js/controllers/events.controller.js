/**
 * Created by andreafspeziale on 24/05/17.
 */
import * as _ from 'lodash'
export default [ '$scope', '$http', function ($scope,$http) {

    $scope.user_country = {
        short_code: '',
        label: ''
    };

    $scope.countries = [
        {
            label: 'Italy',
            short_code: 'it'
        },
        {
            label: 'United Kingdom',
            short_code: 'gb'
        },
        {
            label: 'Slovakia',
            short_code: 'sk'
        },
        {
            label: 'Spain',
            short_code: 'es'
        },
        {
            label: 'All over the World',
            short_code: ''
        }
    ];

    let eventModel = {
        theme : null,
        cursor: 0,
        user_location: null,
        
        prev_cursor : null,
        next_cursor : null,
        
        top:  $(window).scrollTop(),
        data : [],
        
        prev : function () { eventModel.get_events(eventModel.theme, eventModel.user_location, eventModel.prev_cursor) },
        next :function () { eventModel.get_events(eventModel.theme, eventModel.user_location, eventModel.next_cursor) },
        
        get_events : function(theme=eventModel.theme, location=eventModel.user_location, cursor=eventModel.cursor){
            let params = ''
            if (location!=='') params = theme + '/' + location + '/'+ cursor + '/'
            else params = theme + '/' + cursor + '/'

            $http.get('/api/v1.3/events/' + params)
                .then(
                    (response) => {
                        eventModel.prev_cursor = _.get(response, 'data.result.previous_cursor')
                        eventModel.next_cursor = _.get(response, 'data.result.next_cursor')
                        eventModel.data = response.data.result.events
                    },
                    (err)=>{ console.log('ERROR:', err); }
                )
            return eventModel
        },
    }
    
    $scope.EventModel = eventModel

    $scope.$watch('[topic_id,user_country.short_code,user_country.label]', function (newValue, oldValue) {
        if(_.filter($scope.countries, { short_code: newValue[1] }).length == 0) $scope.countries.unshift( { label: newValue[2],  short_code: newValue[1]} )
        $scope.EventModel.theme = newValue[0]
        $scope.EventModel.user_location = newValue[1]
        $scope.EventModel.get_events(newValue[0], newValue[1], -1)
    })

}]