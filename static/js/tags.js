$(function() {
$('.select-tag-form').on('submit', async function(e) {
    e.preventDefault();
    let closestParent = $(this).closest('.select-tag-form');
    const tag_id = closestParent.find(".select-tag").val();
    const user_fav_id = closestParent.find(".user_fav_id").val();
    let res = await axios.post("/api/add-tags", { "user_fav_id" : user_fav_id, "tag_id" : tag_id});
    if(res.data != "Already exists"){
    let closestUL = $(this).closest('tr').find("ul");
    let closestLI = $(closestUL).find('li:first').text();
    if(closestLI == 'No Tags Found'){
    $(closestUL).find('li:first').remove();
    }
    closestUL.append(`<li class="text-success">${res.data}</li>`);
}
});

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
});