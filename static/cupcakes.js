const BASE_URL = "http://localhost:5000/api";


/** given data about a cupcake, generate html */

function generateCupcakeHTML(cupcake) {
  return `
    <div data-cupcake-id=${cupcake.id}>
      <li class="list-group-item">
        Flavor: ${cupcake.flavor} / Size: ${cupcake.size} / Rating: ${cupcake.rating}
        <button class="btn btn-sm btn-danger delete-cupcake">X</button>
      </li>
      <img class="cupcake-img" src="${cupcake.image}" alt="cupcake image">
    </div> 
  `;
}

/** put initial cupcakes on page */
async function showInitialCupcakes() {
  const res = await axios.get(`${BASE_URL}/cupcakes`);

  for (let cupcakeData of res.data.cupcakes) {
    let newCupcake = $(generateCupcakeHTML(cupcakeData));
    $("#cupcakes-list").append(newCupcake);
  }
}

/** handle form for adding of new cupcakes */
$("#new-cupcake-form").on("submit", async function (evt) {
  evt.preventDefault();

  // take in the form data - create variables to hold data
  let flavor = $("#flavor").val();
  let size = $("#size").val();
  let rating = $("#rating").val();
  let image = $("#image").val();

  // construct a new cupcake JSON object from the variables
  const newCupcake = {
    flavor,
    size,
    rating,
    image
  };
  console.log(newCupcake);

  // pass the new cupcake JSON into the axios post request
  // const res = await axios.post(`${BASE_URL}/cupcakes`, newCupcake);
  const res = await axios.post(`${BASE_URL}/cupcakes`, {
    flavor,
    size,
    rating,
    image
  });

  // use the response to create new cupcake's HTML
  let $newCupcakeHTML = $(generateCupcakeHTML(res.data.cupcake));
  $("#cupcakes-list").append($newCupcakeHTML);
  $("new-cupcake-form").trigger("reset");
})

/** handle clicking delete: delete cupcake */
$("#cupcakes-list").on("click", ".delete-cupcake", async function (evt) {
  evt.preventDefault();

  let $cupcake = $(evt.target).closest("div");
  let cupcakeId = $cupcake.data('cupcake-id');

  await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
  $cupcake.remove();
});


$(showInitialCupcakes());