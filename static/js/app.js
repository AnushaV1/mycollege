const $showSingleCollege = $("#single-college");

$('.singlebtn').on("click","button", showCollegeForm);
$('.notes-btn-div').on("click",".notes-btn", addTextField);
$('.notes-btn-div').on("click",".add-field", addNotesBtn);
$('body').on("click",".edit-field", changeNotesBtn);
$('body').on("click",".edit-btn", editNotesBtn);   

function generateNoResultHTML() {
let noresult = `
<div class="container">
<div class="row">
<div class="col-sm-12">
    <h1> NO RESULT FOUND...
    </h1>
</div>
</div>
</div>`;
return noresult;
} 

async function showCollegeForm(evt) {
    
    evt.preventDefault();

    let data = $(this). attr("id");
    
    let res = await axios.get("/api/show-college", {params: {"collegeID": data}});
    
    handleSingleResponse(res)

}
function handleSingleResponse(resp) {
    const data = resp['data']
    
    if(data['success'] = true){
        for(let collegeData of data['colleges']) {  
        let singleMarkupHTML = generateSingleCollegeHTML(collegeData);
        $('.modal-content').html(singleMarkupHTML);
        $('#collegeModal').modal('show'); 
        }
    }
    else {
        let noResultHTML = generateNoResultHTML();
        $showSingleCollege.append(noResultHTML);
        console.log("No results found for this search keywords. Please try with different search terms");
    }
}

function generateSingleCollegeHTML(college) {
    $showSingleCollege.empty();
    const description = college['shortDescription'] ?  college['shortDescription'] : '';
    const college_id = college['collegeUnitId'];
    const acceptanceRate =   (parseFloat(college['acceptanceRate'])* 100).toFixed(2)+"%"
    let similar_colleges = '<p class="text-left"><strong>Similar Colleges</strong></p>';
    if(college['similarColleges']) {
        let similar_list = college['similarColleges'];
        for(let similar of similar_list){
            similar_colleges += '<span class="pull-left">  '+ similar.name + '    '  + similar.city + '       ' + similar.state + '</span><br>';
        }
    } 
    
    let singleMarkup = `
    <div class="modal-header bg-primary">
    <button type="button" class="close" data-dismiss="modal">&times;</button>
    <h4 class="modal-title">${college['name']}</h4>
    <h5>${college['city']} ${college['stateAbbr']}</h5>
    </div>
    <div class="modal-body">
    <div class="row">
    <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6 pull-left">
    <img class="jumbotronwidth" alt="${college['collegeId']}" src="${college['campusImage']}" /></div>
    <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">
        <span>${description}</span>
        <br> <br> <br>
        <span class="h5"><strong>Application Website:<a href="${college['applicationWebsite']}" class="card-link">${college['website']}</a></strong></span>
        <br>
        <span class="h5"><strong>Financial Aid Website:<a href="${college['financialAidWebsite']}" class="card-link">${college['financialAidWebsite']}</a></strong></span>
        <br>
        <span class="h5"><strong>Out of State Tuition:$${college['outOfStateTuition']}</strong></span> 
        <br>
        <span class="h5"><strong>In State Tuition:$${college['inStateTuition']}</strong></span> 
        <br>
        <span class="h5"><strong>Acceptance Rate:${acceptanceRate}</strong></span> 
        <br>
        <span class="h5"><strong>Student Faculty Ratio:${college['studentFacultyRatio']}</strong></span> 
        </div>
    </div>
    </div>
    <div class="modal-footer justify-left bg-info">
    <p class="text-left">${similar_colleges}</p>
</div>`;
        return singleMarkup;
} 

    function addTextField(evt) {
        evt.preventDefault();
        let id = $(this).data('id');
        const div = $(this).closest('div');
        $(this).closest('button').remove();
        $(div).append('<input type="text" name="notes_text" data-id="'+ id + '"/><button class="add-field">Add</button>');
    }
    
    async function addNotesBtn(e){ 
        e.preventDefault(); 
        const input = $(this).siblings('input');
        const text_notes = $(input).val();
        const id = $(input).data('id');
        let response = await axios.post("/api/add-notes", {"notes":text_notes,"id": id});
        if(response['status'] == 200) {
            const update_data = response['data'];
            $(this).closest('td').html('<div class="edit-notes-div">'+ update_data + '<button class="edit-btn" data-notes="'+ text_notes +'" data-id="'+ id +'"> <i class="far fa-edit"></i></button></div>');
        }
    }

    function editNotesBtn(evt) {
        evt.preventDefault();
        let id = $(this).data('id');
        let notes = $(this).data('notes');
        const div = $(this).closest('div');
        $(this).closest('button').remove();
        $(div).html('');
        $(div).append('<input type="text" name="edit_notes" data-id="'+ id + '" value="'+ notes + '"/> <button class="edit-field">Change</button>');
    
    }

    async function changeNotesBtn(e){
        e.preventDefault(); 
        const input = $(this).siblings('input');
        const edit_notes = $(input).val();
        const id = $(input).data('id');
        let response = await axios.post("/api/edit-notes", {"notes":edit_notes,"id": id});
        if(response['status'] == 200) {
            const update_data = response['data'];
            const div_td = $(this).closest('div').html('').append(`<div class="edit-notes-div">${edit_notes}<button class="edit-btn" data-notes="${edit_notes}" data-id="${id}"> <i class="far fa-edit"></i></button></div>`);
        }
    }

