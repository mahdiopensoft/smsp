<template>

  <VContainer>
    <VRow>
      <VCol cols="4">
        <VTable dense>
          <thead>
            <tr>
              <th>الاسم</th>
              <th>النوع</th>
              <th>مطلوب</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in items_table" :key="item.props">
              <td>
                <VCheckbox
                  v-model="filter[item.props]"
                  :label="item.props"
                  hide-details
                  density
                />
              </td>
              <td>[{{ item.type }}]</td>
              <td>{{ item.required }}</td>
            </tr>
          </tbody>
        </VTable>
      </VCol>
      <VCol cols="8">
        <v-card>
          <v-tabs v-model="tab" bg-color="primary">
            <v-tab value="one">Template</v-tab>
            <v-tab value="two">Script</v-tab>
          </v-tabs>

          <v-card-text>
            <v-tabs-window v-model="tab">
              <v-tabs-window-item value="one">
                <custom-data-table v-bind="bindData"/>
              </v-tabs-window-item>

              <v-tabs-window-item value="two" class="bg-cyan-darken-4">
                <pre dir="ltr">
          <code>
&lt;custom-data-table :="{headers , items ,getData  {{ filter.create ?',create:()=>(drawer =true)':''}}  {{filter.edit ?',editItem"':''}} 
{{filter.delete? "delItem: 'url'  or  delItem" :''}} {{ !filter.select?',show-select = false':'' }} ,actionList }" /&gt;
          </code>
          <code>
data(){
  return {
    items: {
      results: [
          { id: 1,name: "samer" },
          ],
      {{ filter.pagination ? 'pagination: { page: 1, perPage: 10, order_data: "", txt_search: "" }' : '' }}
          }
       }
      },
  methods: {
    //required
    async getData(params = this.$params) {
      // params.params.field = "param";      
      return await this.$axios("url", params).then((response) =>this.items = response.data)       
    },
    {{filter.edit ?'editItem(item) { this.data = item;alert("edit") },':''}}
    {{  filter.delete ?'اذا اردت ارسال الدالة بدل الرابط' :''}}
    {{ filter.delete ? 'delItem(id) { return this.$axios.delete("url" + id + "/"),' : '' }}
    {{ filter.delete ? ' .then(e=>{console.log(e)})},' : '' }}       

    اذا كان هناك صفحات مرتبطة بهذه الصفحة يتم ارسال الباراميترات الى الصفحة مع العلم ان الباراميترات 
    arو  en
    اجبارية
    actionList(item) {             
      return {param:value,ar:item.name_ar,en :item.name_en}
   
    }, 

  },
  computed: {
    headers() {
      return [{ title: "الاسم", key: "name" }];
      },
    }
          
          </code>
        </pre>
              </v-tabs-window-item>
            </v-tabs-window>
          </v-card-text>
        </v-card>
      </VCol>
    </VRow>
  </VContainer>
</template>

<script>
export default {
  data() {
    return {
      tab: 0,
      filter: {
        create: false,
        pagination: false,
        select: true,
        edit: false,
        delete: false,
      },
      drawer: false,
      data: {},
      items: {
        results: [
          {
            id: 1,
            name: "samer",
            check: true,
            img:'images/profile/user/app.ico',
            file:'images/profile/user/app.ico',
            list:[1,2,3]
          },
          {
            id: 2,
            name: "ahmed",
            check: false,
            img:'',
            file:'',
            list:['apple','orange','banana']
          },
        ],
      },
      items_table: [
        { props: "pagination", type: "object", required: "no" },
        { props: "create", type: "function", required: "no" },
        { props: "edit", type: "function", required: "no" },
        { props: "delete", type: "string,function", required: "no" },
        { props: "select", type: "boolean", required: "no" },
      ],
    };
  },
  methods: {
    editItem(item) {
      this.data = item;
      alert("edit");
    },
  },
  computed: {
    headers() {
      return [
        { title: "الاسم", key: "name" },
        { title: "Boolean", key: "check" ,type:'check'},
        { title: "صورة", key: "img" ,type:'img'},
        { title: "file", key: "file" ,type:'file'},
        { title: "list", key: "list" ,type:'list'},
      ];
    },
    bindData() {
 
      
      const data = {
        headers: this.headers,
        items: this.items,
        
      };
      if (this.filter.create) data.create = () => alert("create");

      if (this.filter.edit) data.editItem = () => alert("edit");

      if (this.filter.delete) data.delItem = "batch";

      if (!this.filter.select) data.showSelect = false;      
      

      return data;
    },
  },
  watch: {
    "filter.pagination"(val) {
      if (val) {
        this.items.pagination = {
          page: 1,
          perPage: 10,
          order_data: "",
          txt_search: "",
        };
      } else {
        delete this.items.pagination;
      }
    },
  },
};
</script>
