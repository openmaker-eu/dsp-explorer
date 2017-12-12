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
            short_code: 'uk'
        },
        {
            label: 'Slovakia',
            short_code: 'uk'
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

    $scope.EventModel = {
        theme : null,
        cursor: 0,
        user_location: null,
        // current_cursor : null,
        // next_cursor : -1,
        // progress : false,
        top:  $(window).scrollTop(),
        data : [],

        /*
        next : function( theme = this.theme, cursor = this.next_cursor){
            if(
                this.progress === true
                || this.next_cursor == 0
                || this.current_cursor == this.next_cursor
            ) return

            this.progress = true;
            this.current_cursor = this.next_cursor
            this.get_events( theme, cursor )
            return this
            
        },


        reset : function(theme=this.theme, cursor=-1){
            this.data = []
            this.current_cursor = null
            this.next_cursor = -1
            this.next(theme, cursor)
            return this
        },
        */

        get_events : function(theme=this.theme, location=this.user_location, cursor=this.cursor){
            // console.log('get events: ' + theme + '-' + location + '-' + cursor);

            let params = ''

            if (location!='')
                params = theme + '/' + location + '/'+ cursor + '/'
            else
                params = theme + '/' + cursor + '/'

            $http.get('/api/v1.3/events/' + params)
                .then(
                    (response) => {
                        console.log('get events response');
                        console.log(response)
                        this.data = response.data.result.events
                    },
                    (err)=>{ console.log('ERROR:', err); }
                )
            return this
        },
    }

    $scope.$watch('[topic_id,user_country.short_code,user_country.label]', function (newValue, oldValue) {
        if(_.filter($scope.countries, { short_code: newValue[1] }).length == 0) $scope.countries.unshift( { label: newValue[2],  short_code: newValue[1]} )
        $scope.EventModel.theme = newValue[0]
        $scope.EventModel.user_location = newValue[1]
        $scope.EventModel
            .get_events(newValue[0], newValue[1], $scope.cursor)
    })

}]