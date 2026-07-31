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
          <input type="text" placeholder="REQ-001" required />
        </div>
        <div class="field">
          <label>Date of Issue</label>
          <input type="date" />
        </div>
        <div class="field">
          <label>Return Date</label>
          <input type="date" />
        </div>
      </div>
    </div>
    <div class="block-1">
      <h2>Employee Information</h2>
      <div class="grid">
        <div class="field">
          <label> ID <span class="required">*</span></label>
          <input type="text" placeholder="e.g., 01010"  required/>
        </div>
        <div class="field">
          <label>Name</label>
          <input type="text" placeholder="full name" />
        </div>
        <div class="field">
          <label>Email</label>
          <input type="email" placeholder="example@gmail.com" />
        </div>
      </div>
    </div>
    <div class="block-1">
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
            type="text"
            placeholder="Enter Departement"
            class="other-input"
            required
          />
        </div>
        <div class="field">
          <label>Accessory Requested <span class="required">*</span></label>
          <select v-model="Accessory" required>
            <option disabled value="">Select Accessory</option>
            <option v-for="i in Accessories" :key="i" :value="i">
              {{ i }}
            </option>
          </select>
          <input
            v-if="Accessory === 'Other'"
            type="text"
            placeholder="Enter the Accessory"
            class="other-input"
            required
          />
        </div>
        <div class="field">
          <label>Brand/Model</label>
          <input type="text" placeholder="e.g., Logitech G Pro X" />
        </div>
        <div class="field">
          <label>Serial Number</label>
          <input type="text" placeholder="e.g., A3B-0723X-00987" />
        </div>
        <div class="field">
          <label>Quantity <span class="required">*</span></label>
          <input v-model="Quantity" type="number" min="1"  required />
        </div>
        <div class="field">
          <label>Status <span class="required">*</span></label>
          <select v-model="Status" required>
            <option v-for="i in Statuses" :key="i" :value="i">{{ i }}</option>
          </select>
        </div>
      </div>
    </div>
    <div class="block-1">
        <h2>Additional Details</h2>
        <label>Date Issued</label>
        <input type="date" />
        <label> Reason</label>
        <input type="text" placeholder="Enter the reason for the request" />
        <label>Remarks</label>
        <input type="text" placeholder="Additional remarks" />
    </div>
    <div>
      <button>Create Request</button>
      <button>Cancel</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

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
const Accessory = ref("");
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

const Quantity = ref(1);

const Status = ref("Pending");
const Statuses = ["Pending", "Issued", "Returned"];
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

.request > div {
  margin-bottom: 30px;
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

.request button:first-child {
  background: #d71920;
  color: white;
}

.request button:first-child:hover {
  background: #b7151b;
}

.request button:last-child {
  background: #e5e7eb;
  color: #374151;
}

.request button:last-child:hover {
  background: #d1d5db;
}
</style>
