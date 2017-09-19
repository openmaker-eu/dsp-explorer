/**
 * Created by andreafspeziale on 06/07/17.
 */
import * as _ from 'lodash'

export default [ '$scope', function ($scope) {
    
    $scope._ = _
    
    $scope.$watch('birthdate', (a,b) => a===b && ( $scope.birthdate = new Date(a) ) )
    
    $scope.altInputFormats = ['M!/d!/yyyy'];
    $scope.dateOptions = {
        formatYear: 'yy',
        maxDate: new m().subtract(13, 'years'),
        initDate: new Date(new m().subtract(13, 'years')),
        startingDay: 1,
    };
    $scope.datePopup = {opened: false};

    $scope.openDatePopUp = () => $scope.datePopup.opened = true
    $scope.profileImageUpload = n=>$('#profile-image-input').trigger('click')
    
    $scope.checkSocialUrl=(url)=>{
        return (
            url.match(/http:\/\//) || url.match(/https:\/\//) ||
            url.match(/www\./) ||
            url.match(/\.com/) ||
            url.match(/\.it/) ||
            url.match(/\.org/) ||
            url.match(/\.net/)
        )
    }
    
    $scope.addHttpToSocialUrl =(url)=>{
        if( !url.match(/http:\/\//) && !url.match(/https:\/\//) ) url = 'https://'+url;
        return url
    }
    
    $scope.extractUserFromSocialUrl =(url)=>{
        
        if( url.match(/http:\/\//) || url.match(/https:\/\//) ) url = url.replace('https://', '') && url.replace('http://', '')
        if( url.match(/www\./)) url = url.replace('www.', '')
        if( url.match(/www\./)) url = url.replace('www.', '')
        if( url.match(/\.com/)) url = url.replace('.com', '')
        if( url.match(/\.it/)) url = url.replace('.it', '')
        if( url.match(/\.org/)) url = url.replace('.org', '')
        if( url.match(/\.net/)) url = url.replace('.net', '')
    
        let user = url.replace(/\/$/, '').split('/').pop().trim()
        return user !== '' ? user : url ;
    }

}]