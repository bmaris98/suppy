var data = '{"project_name": "Demo1", "stats": [{"active_time": 0, "has_calibration": false, "idle_time": 48880000, "name": "Aluminiu", "not_used_resources": 0, "resource_count": 20, "resource_type": "Lingou Alu", "runs": 20, "semi_finite": [], "total_cost": 0, "type": "start", "uid": "1589144228.330096"}, {"active_time": 0, "has_calibration": false, "idle_time": 48880000, "name": "Manere", "not_used_resources": 0, "resource_count": 30, "resource_type": "Maner", "runs": 30, "semi_finite": [], "total_cost": 0, "type": "start", "uid": "1589144230.041849"}, {"active_time": 0, "has_calibration": false, "idle_time": 48880000, "name": "Nituri", "not_used_resources": 0, "resource_count": 30, "resource_type": "Nit", "runs": 30, "semi_finite": [], "total_cost": 0, "type": "start", "uid": "1589144348.265267"}, {"active_time": 2400, "has_calibration": false, "idle_time": 48877600, "name": "Banda Transportoare", "runs": 20, "semi_finite": [], "total_cost": 20, "type": "transport", "uid": "1589144359.930066"}, {"active_time": 2400000, "calibration_count": 0, "calibration_left": 9979, "calibration_time": 0, "has_calibration": true, "idle_time": 46480000, "name": "Masina Injectie", "runs": 20, "semi_finite": [], "total_calibration_cost": 0, "total_cost": 20, "type": "custom", "uid": "1589144397.041948"}, {"active_time": 2400, "has_calibration": false, "idle_time": 48877600, "name": "Brat Robot 1", "runs": 20, "semi_finite": [], "total_cost": 0, "type": "transport", "uid": "1589144527.161676"}, {"active_time": 200000, "calibration_count": 1, "calibration_left": 20, "calibration_time": 1200000, "has_calibration": true, "idle_time": 47480000, "name": "Masina de stantat", "runs": 20, "semi_finite": [], "total_calibration_cost": 30, "total_cost": 60, "type": "custom", "uid": "1589144540.769882"}, {"active_time": 0, "has_calibration": false, "idle_time": 48880000, "name": "Nituri2", "not_used_resources": 0, "resource_count": 30, "resource_type": "Nit", "runs": 30, "semi_finite": [], "total_cost": 0, "type": "start", "uid": "1589144724.866438"}, {"active_time": 2280, "has_calibration": false, "idle_time": 48877720, "name": "Brat Robot Q", "runs": 19, "semi_finite": [], "total_cost": 19, "type": "transport", "uid": "1589144781.361851"}, {"active_time": 3000, "calibration_count": 3, "calibration_left": 6, "calibration_time": 1200, "has_calibration": true, "idle_time": 48875800, "name": "Nituri in maner", "runs": 30, "semi_finite": [], "total_calibration_cost": 9, "total_cost": 90, "type": "custom", "uid": "1589144797.576716"}, {"active_time": 420, "has_calibration": false, "idle_time": 48879580, "name": "Brat robot", "runs": 21, "semi_finite": [{"_category": "MANERE_CU_NIT", "_errors": []}, {"_category": "MANERE_CU_NIT", "_errors": []}], "total_cost": 21, "type": "transport", "uid": "1589144833.569316"}, {"active_time": 1900, "calibration_count": 0, "calibration_left": 6, "calibration_time": 0, "has_calibration": true, "idle_time": 48878100, "name": "Masa asamblare finala", "runs": 19, "semi_finite": [], "total_calibration_cost": 0, "total_cost": 57, "type": "custom", "uid": "1589144839.081639"}, {"active_time": 0, "capacity": 10, "has_calibration": false, "idle_time": 48880000, "name": "Depozit intermediar", "runs": 33, "semi_finite": [{"_category": "MANERE_CU_NIT", "_errors": []}, {"_category": "MANERE_CU_NIT", "_errors": []}], "total_cost": 0, "type": "buffer", "uid": "1589144910.122335", "was_full": true}, {"active_time": 0, "has_calibration": false, "idle_time": 48880000, "name": "Erori fisura", "runs": 20, "semi_finite": [], "total_cost": 0, "type": "random_error", "uid": "1589144939.937978"}, {"active_time": 0, "has_calibration": false, "idle_time": 48880000, "name": "Etanseitate Nituire", "runs": 19, "semi_finite": [], "total_cost": 0, "type": "random_error", "uid": "1589144941.266601"}, {"active_time": 2000, "calibration_count": 2, "calibration_left": 10, "calibration_time": 120000, "errors_found": 1, "errors_missed": 0, "has_calibration": true, "idle_time": 48758000, "name": "Test Fisura", "runs": 20, "semi_finite": [], "total_calibration_cost": 10, "total_cost": 20, "type": "test", "uid": "1589145031.994232", "with_error_count": 1, "without_error_count": 19}, {"active_time": 0, "has_calibration": false, "idle_time": 48880000, "name": "Start + Err", "runs": 20, "semi_finite": [], "total_cost": 0, "type": "convergence", "uid": "1589145058.450312"}, {"active_time": 19000, "calibration_count": 0, "calibration_left": 6, "calibration_time": 0, "errors_found": 2, "errors_missed": 0, "has_calibration": true, "idle_time": 48861000, "name": "Test Etanseitate", "runs": 19, "semi_finite": [], "total_calibration_cost": 0, "total_cost": 38, "type": "test", "uid": "1589145267.074516", "with_error_count": 2, "without_error_count": 17}, {"active_time": 0, "errors": {"ETAN": 2}, "has_calibration": false, "idle_time": 48880000, "name": "Depozit", "resource_count": 49, "resources": [{"_category": "Nit", "_errors": []}, {"_category": "Nit", "_errors": []}, {"_category": "Nit", "_errors": []}, {"_category": "ASAMBLAT", "_errors": []}, {"_category": "ASAMBLAT", "_errors": []}, {"_category": "ASAMBLAT", "_errors": []}, {"_category": "ASAMBLAT", "_errors": ["ETAN"]}, {"_category": "ASAMBLAT", "_errors": []}, {"_category": "ASAMBLAT", "_errors": []}, {"_category": "ASAMBLAT", "_errors": []}, {"_category": "ASAMBLAT", "_errors": []}, {"_category": "ASAMBLAT", "_errors": []}, {"_category": "ASAMBLAT", "_errors": []}, {"_category": "ASAMBLAT", "_errors": []}, {"_category": "ASAMBLAT", "_errors": []}, {"_category": "ASAMBLAT", "_errors": ["ETAN"]}, {"_category": "ASAMBLAT", "_errors": []}, {"_category": "ASAMBLAT", "_errors": []}, {"_category": "ASAMBLAT", "_errors": []}, {"_category": "ASAMBLAT", "_errors": []}, {"_category": "ASAMBLAT", "_errors": []}, {"_category": "ASAMBLAT", "_errors": []}, {"_category": "Nit", "_errors": []}, {"_category": "Nit", "_errors": []}, {"_category": "Nit", "_errors": []}, {"_category": "Nit", "_errors": []}, {"_category": "Nit", "_errors": []}, {"_category": "Nit", "_errors": []}, {"_category": "Nit", "_errors": []}, {"_category": "Nit", "_errors": []}, {"_category": "Nit", "_errors": []}, {"_category": "Nit", "_errors": []}, {"_category": "Nit", "_errors": []}, {"_category": "Nit", "_errors": []}, {"_category": "Nit", "_errors": []}, {"_category": "Nit", "_errors": []}, {"_category": "Nit", "_errors": []}, {"_category": "Nit", "_errors": []}, {"_category": "Nit", "_errors": []}, {"_category": "Nit", "_errors": []}, {"_category": "Nit", "_errors": []}, {"_category": "Nit", "_errors": []}, {"_category": "Nit", "_errors": []}, {"_category": "Nit", "_errors": []}, {"_category": "Nit", "_errors": []}, {"_category": "Nit", "_errors": []}, {"_category": "Nit", "_errors": []}, {"_category": "Nit", "_errors": []}, {"_category": "Nit", "_errors": []}], "runs": 49, "semi_finite": [], "total_cost": 0, "type": "end", "uid": "1589145380.146341", "valid_resource_count": 47}, {"active_time": 47000000, "calibration_count": 47, "calibration_left": 1, "calibration_time": 1880000, "has_calibration": true, "idle_time": 0, "name": "Reparare Etan", "non_repairs": 47, "repairs": 0, "runs": 47, "semi_finite": [], "total_calibration_cost": 235, "total_cost": 1175, "type": "repair", "uid": "1589145827.618106"}, {"active_time": 0, "has_calibration": false, "idle_time": 48880000, "name": "Nituri", "not_used_resources": 0, "resource_count": 30, "resource_type": "Nit", "runs": 30, "semi_finite": [], "total_cost": 0, "type": "start", "uid": "1589145839.066367"}, {"active_time": 0, "has_calibration": false, "idle_time": 48880000, "name": "Confluence", "runs": 47, "semi_finite": [], "total_cost": 0, "type": "convergence", "uid": "1589145900.322896"}, {"active_time": 0, "has_calibration": false, "idle_time": 48880000, "name": "Confluence", "runs": 49, "semi_finite": [], "total_cost": 0, "type": "convergence", "uid": "1589145970.490244"}, {"active_time": 0, "capacity": 200, "has_calibration": false, "idle_time": 48880000, "name": "TMP", "runs": 1, "semi_finite": [], "total_cost": 0, "type": "buffer", "uid": "1589147458.002859", "was_full": false}, {"active_time": 0, "has_calibration": false, "idle_time": 48880000, "name": "Start", "not_used_resources": 0, "resource_count": 30, "resource_type": "TypeA", "runs": 30, "semi_finite": [], "total_cost": 0, "type": "start", "uid": "1589148098.651365"}, {"active_time": 0, "has_calibration": false, "idle_time": 48880000, "name": "Confluence", "runs": 31, "semi_finite": [], "total_cost": 0, "type": "convergence", "uid": "1589148101.282446"}, {"active_time": 0, "errors": {"FISURA": 1}, "has_calibration": false, "idle_time": 48880000, "name": "Warehouse", "resource_count": 31, "resources": [{"_category": "TypeA", "_errors": []}, {"_category": "TypeA", "_errors": []}, {"_category": "TypeA", "_errors": []}, {"_category": "TypeA", "_errors": []}, {"_category": "TypeA", "_errors": []}, {"_category": "TypeA", "_errors": []}, {"_category": "TypeA", "_errors": []}, {"_category": "TypeA", "_errors": []}, {"_category": "TypeA", "_errors": []}, {"_category": "TypeA", "_errors": []}, {"_category": "TypeA", "_errors": []}, {"_category": "TypeA", "_errors": []}, {"_category": "TypeA", "_errors": []}, {"_category": "TypeA", "_errors": []}, {"_category": "TypeA", "_errors": []}, {"_category": "TypeA", "_errors": []}, {"_category": "TypeA", "_errors": []}, {"_category": "TypeA", "_errors": []}, {"_category": "TypeA", "_errors": []}, {"_category": "TypeA", "_errors": []}, {"_category": "TypeA", "_errors": []}, {"_category": "TypeA", "_errors": []}, {"_category": "TypeA", "_errors": []}, {"_category": "TypeA", "_errors": []}, {"_category": "TypeA", "_errors": []}, {"_category": "TypeA", "_errors": []}, {"_category": "TypeA", "_errors": []}, {"_category": "TypeA", "_errors": []}, {"_category": "TypeA", "_errors": []}, {"_category": "TypeA", "_errors": []}, {"_category": "Stantate", "_errors": ["FISURA"]}], "runs": 31, "semi_finite": [], "total_cost": 0, "type": "end", "uid": "1589148114.010425", "valid_resource_count": 30}], "time": 48880000}';