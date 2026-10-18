<template>
    <h3 class="mt-2">{{item.model}}</h3>ssaa
      <v-table class="custom-data-table w-100" >
        <thead>
          <tr>
            <th>المعرف</th>
            <th>العنصر</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <template
              v-for="(value, key) in item.related_objects"
              :key="key"
            >
              <td>
                {{ value.id }}
              </td>
              <td>
                {{ value.object_str }}
              </td>
            </template>
          </tr>
        </tbody>
      </v-table>
    
</template>
<script>
export default {
    
}
</script>