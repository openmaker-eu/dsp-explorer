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
    $scope.profileImageUpload = () => $('#profile-image-input').trigger('click')

    $scope.previewImage = (input) => {

        if (input.files && input.files[0]) {
            
            var reader = new FileReader();
            
            reader.onload = (e) => {
                let image = $('#profile-image');
                $scope.fitImageToCircle(image)
                image.attr('src', e.target.result)
    
            }
            reader.readAsDataURL(input.files[0]);
            
        }
    }
    
    $scope.fitImageToCircle = (image)=> {
        
        image.removeAttr('style').hide(0)
        image.on('load', ()=>{
        
            let width = image.get(0).naturalWidth
            let height = image.get(0).naturalHeight
        
            let css = {'display':'block', 'position': 'absolute'}
            width > height? css.height = '100%' : css.width = '100%'
            image.css(css).show(0)
        
        })
    }
    
    $scope.fitImageToCircle($('#profile-image'))
    $scope.fitImageToCircle($('.profile-image-static img'))
    
    $scope.checkSocialUrl =(url)=>{
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