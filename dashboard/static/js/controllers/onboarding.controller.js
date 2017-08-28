/**
 * Created by andreafspeziale on 06/07/17.
 */
export default [ '$scope', function ($scope) {
    
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
    
    $scope.occupation = {
        selected : '',
        available : [
            'Entrepreneur',
            'Manager',
            'Employee',
            'Free-lance',
            'Researcher',
            'Policy-Maker',
            'Student',
            'Other'
        ]
    };
    $scope.sector = {
        selected : '',
        available : [
            'Food industries',
            'Textiles and clothing industries',
            'Wood and furniture industries',
            'Paper and printing industries',
            'Jewelry industries',
            'Mining and mineral processing industries',
            'Electrical and electronic industries',
            'Metal Industries',
            'Engineering industries',
            'Chemicals and Drugs industries',
            'Rubber and plastic industries',
            'Public utilities',
            'Constructions',
            'Other manufacturing'
        ]
    };
    $scope.size = {
        selected : '',
        available : [
            'A micro enterprise (<10 staff)',
            'A small enterprise (<50 staff)',
            'A medium enterprise (<250 staff)',
            'A large enterprise (>250 staff)'
        ]
    };
    $scope.types_of_innovation = {
        selected: '',
        available : [
            'Product innovation',
            'Process innovation',
            'Technological innovation',
            'Business model innovation',
            'Social innovation'
        ]
    };
    

}]