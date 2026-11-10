 <template>
  <drawer
    :data="data"
    click="/user-manager/users/"
    :getData="getData"
    :files="['image_user']"
    :items="items"
  >
    <template v-slot>
      <add-to-level
        v-if="!data.id"
        :data="data"
        />
      <fields
        :data="data"
        url="users"
        :attr="{
          first_name: { rules: [$required ] },
          last_name: { rules: [$required] },
          email: { rules: [$email,$max_length(255)] },
          fk_organization: {
            param: this.data.fk_organization__company_level,
            depend: data.active_level && !data.id,
          },
          fk_organization__company_level: {
            depend: data.active_level && !data.id,
          },
          groups:{
            rules: [$required],
          },
        }"
        ><template v-slot="{ field }">
          <VSheet v-if="field.name === 'password'">
            <custom-text-field
              v-if="!data.id"
              type="password"
              :rules="[$required]"
              v-model="data.password"
              label=" كلمة المرور"
            ></custom-text-field>
            <custom-text-field
              v-if="!data.id"
              type="password"
              :rules="confirmPassword"
              v-model="password2"
              label="تاكيد كلمة المرور"
            ></custom-text-field>
          </VSheet> </template
      ></fields>
    </template>
  </drawer>
</template>
<script>
export default {
  props: {
    data: Object,
    items: [Array, Object],
  },
  data() {
    return {
      password2: "",
      confirmPassword: [
        (v) => !!v || "يجب تاكيد كلمة المرور",
        (v) => v === this.data.password || "كلمات المرور غير متطابقة",
      ],
    };
  },
};
</script>
