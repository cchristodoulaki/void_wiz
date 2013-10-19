/* 
# Author: Christina Christodoulakis
# 
#    Copyright 2013 Christina Christodoulakis
# 
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
# 
#        http://www.apache.org/licenses/LICENSE-2.0
# 
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
 */
package entity_layer;


/**
 *
 * @author Christina Christodoulakis
 * @email christina'@'cs.toronto.edu 
 * Computer Science, University of Toronto 2013
 */
public class PatientVisit {
    private Integer visit_id;
    private String doctorName;
    private String patientName;
    private String diagnosis;
    private String treatment;
    
    public PatientVisit(){}

    public PatientVisit(String doctorName, String patientName, String diagnosis, String treatment) {
        this.doctorName = doctorName;
        this.patientName = patientName;
        this.diagnosis = diagnosis;
        this.treatment = treatment;
    }

    public PatientVisit(Integer visit_id, String doctorName, String patientName, String diagnosis, String treatment) {
        this.visit_id = visit_id;
        this.doctorName = doctorName;
        this.patientName = patientName;
        this.diagnosis = diagnosis;
        this.treatment = treatment;
    }
    
    public Integer getVisit_id() {
        return visit_id;
    }

    public void setVisit_id(Integer visit_id) {
        this.visit_id = visit_id;
    }

    public String getDoctorName() {
        return doctorName;
    }

    public void setDoctorName(String doctorName) {
        this.doctorName = doctorName;
    }

    public String getPatientName() {
        return patientName;
    }

    public void setPatientName(String patientName) {
        this.patientName = patientName;
    }

    public String getDiagnosis() {
        return diagnosis;
    }

    public void setDiagnosis(String diagnosis) {
        this.diagnosis = diagnosis;
    }

    public String getTreatment() {
        return treatment;
    }

    public void setTreatment(String treatment) {
        this.treatment = treatment;
    }
    
    
}
