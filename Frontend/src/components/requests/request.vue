<template>
  <div class="request">
    <div>
      <h1>New Equipment Request</h1>
      <h2>Fill in the form to create a new equipment request</h2>
    </div>
    <div class="block-1">
      <h2>Request information</h2>
      <div class="grid">
        <div class="field">
          <label> Request ID <span class="required">*</span></label>
          <input
            v-model="request_id"
            type="text"
            placeholder="REQ-001"
            required
          />
        </div>
        <div class="field">
          <label>Date of Issue</label>
          <input v-model="issue_date" type="date" />
        </div>
        <div class="field">
          <label>Return Date</label>
          <input v-model="return_date" type="date" />
        </div>
      </div>
    </div>
    <div class="block-1">
      <h2>Employee Information</h2>
      <div class="grid">
        <div class="field">
          <label> ID <span class="required">*</span></label>
          <input
            v-model="employee_id"
            type="text"
            placeholder="e.g., 01010"
            required
          />
        </div>
        <div class="field">
          <label>Name</label>
          <input v-model="employee_name" type="text" placeholder="full name" />
        </div>
        <div class="field">
          <label>Email</label>
          <input
            v-model="employee_email"
            type="email"
            placeholder="example@gmail.com"
          />
        </div>
      </div>
    </div>
    <div class="block-1" v-for="(equipment, index) in equipement" :key="index">
      <h2>Equipment Details</h2>
      <div class="grid">
        <div class="field">
          <label>Departement <span class="required">*</span></label>
          <select v-model="Dep" required>
            <option disabled value="">Select Departement</option>
            <option v-for="i in departement" :key="i" :value="i">
              {{ i }}
            </option>
          </select>
          <input
            v-if="Dep === 'Other'"
            v-model="otherDepartment"
            type="text"
            placeholder="Enter Departement"
            class="other-input"
            required
          />
        </div>
        <div class="field">
          <label>Accessory Requested <span class="required">*</span></label>
          <select v-model="equipment.accessory_req" required>
            <option disabled value="">Select Accessory</option>
            <option v-for="i in Accessories" :key="i" :value="i">
              {{ i }}
            </option>
          </select>
          <input
            v-if="equipment.accessory_req === 'Other'"
            v-model="otherAccess"
            type="text"
            placeholder="Enter the Accessory"
            class="other-input"
            required
          />
        </div>
        <div class="field">
          <label>Brand/Model</label>
          <input
            v-model="equipment.brand_model"
            type="text"
            placeholder="e.g., Logitech G Pro X"
          />
        </div>
        <div class="field">
          <label>Serial Number</label>
          <input
            v-model="equipment.serial_Number"
            type="text"
            placeholder="e.g., A3B-0723X-00987"
          />
        </div>
        <div class="field">
          <label>Quantity <span class="required">*</span></label>
          <input v-model="equipment.quantity" type="number" min="1" required />
        </div>
        <div class="field">
          <label>Status <span class="required">*</span></label>
          <select v-model="equipment.status" required>
            <option v-for="i in Statuses" :key="i" :value="i">{{ i }}</option>
          </select>
        </div>
      </div>
    </div>
    <div class="block-1">
      <h2>Additional Details</h2>
      <label>Date Issued</label>
      <input v-model="date_issued" type="date" />
      <label> Reason</label>
      <input
        v-model="reason"
        type="text"
        placeholder="Enter the reason for the request"
      />
      <label>Remarks</label>
      <input v-model="remarks" type="text" placeholder="Additional remarks" />
    </div>
    <div class="actions">
      <button @click="add_equipement" class="add-equip-btn">
        Add Equipment
      </button>

      <div class="right-actions">
        <button @click="createRequest" class="create-btn">
          {{ props.editRequest ? "Modify Request" : "Create Request" }}
        </button>
        <button class="cancel-btn">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch , onMounted } from "vue";
import { useRouter } from "vue-router";
import { create_request, update_request ,get_requests} from "../../services/request.service";
import { get_equipments, type Equipment } from "../../services/equipment.service";

interface RequestItem {
  id: number;
  status: string;
  accessory_req: string;
  brand_model: string;
  serial_Number: string;
  quantity: number;
  request: number;
}

interface Request {
  id: number;
  request_id: string;
  issue_date: string | null;
  return_date: string | null;
  employee_id: string;
  employee_name: string;
  employee_email: string;
  department: string;
  reason: string;
  remarks: string;
  date_issued: string | null;
  created_at: string;
  updated_at: string;
  created_by: string;
  based_on_stock: boolean;
  items: RequestItem[];
}
const props = defineProps<{
  editRequest?: Request;
}>();
const router = useRouter();
const emit = defineEmits(["created"]);

const request_id = ref("");
const issue_date = ref("");
const return_date = ref("");
const date_issued = ref("");
const employee_id = ref("");
const employee_name = ref("");
const employee_email = ref("");
const reason = ref("");
const remarks = ref("");

const equipmentsStock = ref<Equipment[]>([]);
const generateNextRequestId = async () => {
  try {
    const response = await get_requests();

    const requests = response.data;

    let maxNumber = 0;

    for (const request of requests) {
      const match = request.request_id?.match(/^REQ-(\d+)$/);

      if (match) {
        const number = parseInt(match[1], 10);

        if (number > maxNumber) {
          maxNumber = number;
        }
      }
    }

    const nextNumber = maxNumber + 1;

    request_id.value = `REQ-${String(nextNumber).padStart(4, "0")}`;
  } catch (error) {
    console.error("Error generating Request ID:", error);

    request_id.value = "REQ-0001";
  }
};


const otherDepartment = ref("");
const otherAccess = ref("");

const checkStock = () => {
  const insufficientItems: string[] = [];

  for (const equipment of equipement.value) {
    const stockItem = equipmentsStock.value.find(
      (item) =>
        item.category === equipment.accessory_req &&
        item.status === "Available",
    );

    const availableQuantity = stockItem?.quantity ?? 0;

    if (equipment.quantity > availableQuantity) {
      insufficientItems.push(
        `${equipment.accessory_req} (demandé: ${equipment.quantity}, disponible: ${availableQuantity})`,
      );
    }
  }

  return insufficientItems;
};

const createRequest = async () => {
  if (!request_id.value) {
    alert("Request ID is required");
    return;
  }

  if (!employee_id.value) {
    alert("Employee ID is required");
    return;
  }

  if (!Dep.value) {
    alert("Department is required");
    return;
  }

  for (const equipment of equipement.value) {
    if (!equipment.accessory_req) {
      alert("Accessory Requested is required");
      return;
    }

    if (!equipment.quantity) {
      alert("Quantity is required");
      return;
    }

    if (!equipment.status) {
      alert("Status is required");
      return;
    }
  }

  // Vérification du stock uniquement si Based on stock est activé
if (based_on_stock.value) {
  for (const equipment of equipement.value) {
    const availableStock = getAvailableStock(
      equipment.accessory_req
    );

    if (
      equipment.status === "Issued" &&
      equipment.quantity > availableStock
    ) {
      alert(
        `${equipment.accessory_req} is insufficient in stock.\n` +
        `Available: ${availableStock}\n` +
        `Requested: ${equipment.quantity}\n\n` +
        `The request will still be created.`
      );
    }
  }
}

  try {
    const data = {
      request_id: request_id.value,
      issue_date: issue_date.value || null,
      return_date: return_date.value || null,
      date_issued: date_issued.value || null,

      employee_id: employee_id.value,
      employee_name: employee_name.value,
      employee_email: employee_email.value,

      department:
        Dep.value === "Other"
          ? otherDepartment.value
          : Dep.value,

      reason: reason.value,
      remarks: remarks.value,

      based_on_stock: based_on_stock.value,

      items: equipement.value.map((equipment) => ({
        ...equipment,
        accessory_req:
          equipment.accessory_req === "Other"
            ? otherAccess.value
            : equipment.accessory_req,
      })),
    };

    if (props.editRequest) {
      await update_request(props.editRequest.id, data);
      alert("Request modified successfully");
    } else {
      await create_request(data);
      alert("Request created successfully");
    }

    emit("created");

  } catch (error: any) {
    console.error("BACKEND ERROR:", error);

    alert(
      props.editRequest
        ? "Failed to modify request."
        : "Failed to create request.",
    );
  }
};


const loadStock = async () => {
  try {
    const response = await get_equipments();
    equipmentsStock.value = response.data;
  } catch (error) {
    console.error("Error loading stock:", error);
  }
};

const Dep = ref("");
const departement = [
  "Engineering",
  "Finance",
  "HR",
  "IT",
  "Logistic",
  "Marketing",
  "Operations",
  "sales",
  "Other",
];

const equipement = ref([
  {
    accessory_req: "",
    quantity: 1,
    status: "Pending",
    brand_model: "",
    serial_Number: "",
  },
]);

const add_equipement = () => {
  equipement.value.push({
    accessory_req: "",
    quantity: 1,
    status: "Pending",
    brand_model: "",
    serial_Number: "",
  });
};
// const Accessory = ref("");
// const Quantity = ref(1);
// const Status = ref("Pending");
const Accessories = [
  "Headset",
  "Mouse",
  "Keyboard",
  "Laptop",
  "Desktop",
  "Monitor",
  "WebCam",
  "Other",
];
const Statuses = ["Pending", "Issued", "Returned"];

const based_on_stock = ref(false);

onMounted(() => {
  loadStock();

  const savedSetting = localStorage.getItem("based_on_stock");

  if (savedSetting !== null) {
    based_on_stock.value = savedSetting === "true";
  }
});

watch(
  () => props.editRequest,
  async (request) => {
    // =========================
    // MODE MODIFICATION
    // =========================
    if (request) {
      request_id.value = request.request_id;

      based_on_stock.value = request.based_on_stock;
      issue_date.value = request.issue_date || "";
      return_date.value = request.return_date || "";
      date_issued.value = request.date_issued || "";

      employee_id.value = request.employee_id;
      employee_name.value = request.employee_name;
      employee_email.value = request.employee_email;

      reason.value = request.reason;
      remarks.value = request.remarks;

      Dep.value = request.department;

      equipement.value = request.items.map((item) => ({
        accessory_req: item.accessory_req,
        quantity: item.quantity,
        status: item.status,
        brand_model: item.brand_model,
        serial_Number: item.serial_Number,
      }));

      return;
    }

    // =========================
    // MODE NOUVELLE REQUEST
    // =========================
    await generateNextRequestId();
  },
  { immediate: true },
);

const getAvailableStock = (category: string) => {
  return equipmentsStock.value
    .filter(
      (equipment) =>
        equipment.category === category &&
        equipment.status === "Available",
    )
    .reduce((total, equipment) => total + equipment.quantity, 0);
};

</script>

<style scoped>
.block-1 {
  margin-bottom: 30px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.field {
  display: flex;
  flex-direction: column;
}
.request {
  max-width: 2000px;
  margin: 30px auto;
  padding: 30px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.request h1 {
  margin-bottom: 10px;
  color: #1f2937;
  font-size: 30px;
}

.other-input {
  margin-top: 12px;
}

.request h2 {
  margin-bottom: 20px;
  color: #374151;
  font-size: 20px;
}

.request label {
  display: block;
  margin-bottom: 8px;
  margin-top: 15px;
  font-weight: 600;
  color: #374151;
}

.request input,
.request select,
.request textarea {
  width: 100%;
  padding: 18px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 15px;
  box-sizing: border-box;
  transition: 0.3s;
}
.required {
  color: red;
}
.request input:focus,
.request select:focus,
.request textarea:focus {
  border-color: #d71920;
  outline: none;
  box-shadow: 0 0 5px rgba(215, 25, 32, 0.3);
}

.request input::placeholder {
  color: #9ca3af;
}

.request > div:not(:first-child) {
  padding: 20px;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  background: #f9fafb;
}

.request > div:last-child {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  border: none;
  background: transparent;
  padding: 0;
}

.request button {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.3s;
  width: 250px;
  height: 60px;
}
.actions {
  display: flex;
  justify-content: space-between;
  align-items: center;

  width: 100%;
  margin: 0 !important;
  padding: 0 !important;

  border: none !important;
  background: transparent !important;
}

.right-actions {
  display: flex;
  align-items: center;
  gap: 15px;
  margin: 0 !important;
}

/* Style général des boutons */
.actions button {
  width: 180px;
  height: 50px;
  padding: 12px 24px;

  border-radius: 8px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;

  transition: 0.2s;
}

/* Add Equipment */
.add-equip-btn {
  margin-right: auto;
  background: white !important;
  color: #d71920 !important;
  border: 2px solid #d71920 !important;
}

.add-equip-btn:hover {
  background: #d71920 !important;
  color: white !important;
}

/* Create Request */
.create-btn {
  background: #d71920 !important;
  color: white !important;
  border: 2px solid #d71920 !important;
}

.create-btn:hover {
  background: #b7151b !important;
}

/* Cancel */
.cancel-btn {
  background: #e5e7eb !important;
  color: #374151 !important;
  border: 2px solid #e5e7eb !important;
}

.cancel-btn:hover {
  background: #d1d5db !important;
}
.field:has(input[type="checkbox"]) {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 14px 16px;
}

.field:has(input[type="checkbox"]) label {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
  cursor: pointer;
}

.field:has(input[type="checkbox"]) input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.field:has(input[type="checkbox"]) small {
  display: block;
  margin-top: 8px;
  margin-left: 28px;
  color: #64748b;
  font-size: 12px;
}
</style>
