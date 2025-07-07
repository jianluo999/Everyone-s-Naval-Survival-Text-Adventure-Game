@echo off
echo 开始批量导入数据...

echo 导入场景批次 1/17...
mysql -u root -pmgsincos30 < scenes_batch_001.sql
if %errorlevel% neq 0 (
    echo 场景批次 1 导入失败！
    pause
    exit /b 1
)

echo 导入场景批次 2/17...
mysql -u root -pmgsincos30 < scenes_batch_002.sql
if %errorlevel% neq 0 (
    echo 场景批次 2 导入失败！
    pause
    exit /b 1
)

echo 导入场景批次 3/17...
mysql -u root -pmgsincos30 < scenes_batch_003.sql
if %errorlevel% neq 0 (
    echo 场景批次 3 导入失败！
    pause
    exit /b 1
)

echo 导入场景批次 4/17...
mysql -u root -pmgsincos30 < scenes_batch_004.sql
if %errorlevel% neq 0 (
    echo 场景批次 4 导入失败！
    pause
    exit /b 1
)

echo 导入场景批次 5/17...
mysql -u root -pmgsincos30 < scenes_batch_005.sql
if %errorlevel% neq 0 (
    echo 场景批次 5 导入失败！
    pause
    exit /b 1
)

echo 导入场景批次 6/17...
mysql -u root -pmgsincos30 < scenes_batch_006.sql
if %errorlevel% neq 0 (
    echo 场景批次 6 导入失败！
    pause
    exit /b 1
)

echo 导入场景批次 7/17...
mysql -u root -pmgsincos30 < scenes_batch_007.sql
if %errorlevel% neq 0 (
    echo 场景批次 7 导入失败！
    pause
    exit /b 1
)

echo 导入场景批次 8/17...
mysql -u root -pmgsincos30 < scenes_batch_008.sql
if %errorlevel% neq 0 (
    echo 场景批次 8 导入失败！
    pause
    exit /b 1
)

echo 导入场景批次 9/17...
mysql -u root -pmgsincos30 < scenes_batch_009.sql
if %errorlevel% neq 0 (
    echo 场景批次 9 导入失败！
    pause
    exit /b 1
)

echo 导入场景批次 10/17...
mysql -u root -pmgsincos30 < scenes_batch_010.sql
if %errorlevel% neq 0 (
    echo 场景批次 10 导入失败！
    pause
    exit /b 1
)

echo 导入场景批次 11/17...
mysql -u root -pmgsincos30 < scenes_batch_011.sql
if %errorlevel% neq 0 (
    echo 场景批次 11 导入失败！
    pause
    exit /b 1
)

echo 导入场景批次 12/17...
mysql -u root -pmgsincos30 < scenes_batch_012.sql
if %errorlevel% neq 0 (
    echo 场景批次 12 导入失败！
    pause
    exit /b 1
)

echo 导入场景批次 13/17...
mysql -u root -pmgsincos30 < scenes_batch_013.sql
if %errorlevel% neq 0 (
    echo 场景批次 13 导入失败！
    pause
    exit /b 1
)

echo 导入场景批次 14/17...
mysql -u root -pmgsincos30 < scenes_batch_014.sql
if %errorlevel% neq 0 (
    echo 场景批次 14 导入失败！
    pause
    exit /b 1
)

echo 导入场景批次 15/17...
mysql -u root -pmgsincos30 < scenes_batch_015.sql
if %errorlevel% neq 0 (
    echo 场景批次 15 导入失败！
    pause
    exit /b 1
)

echo 导入场景批次 16/17...
mysql -u root -pmgsincos30 < scenes_batch_016.sql
if %errorlevel% neq 0 (
    echo 场景批次 16 导入失败！
    pause
    exit /b 1
)

echo 导入场景批次 17/17...
mysql -u root -pmgsincos30 < scenes_batch_017.sql
if %errorlevel% neq 0 (
    echo 场景批次 17 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 1/67...
mysql -u root -pmgsincos30 < choices_batch_001.sql
if %errorlevel% neq 0 (
    echo 选择批次 1 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 2/67...
mysql -u root -pmgsincos30 < choices_batch_002.sql
if %errorlevel% neq 0 (
    echo 选择批次 2 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 3/67...
mysql -u root -pmgsincos30 < choices_batch_003.sql
if %errorlevel% neq 0 (
    echo 选择批次 3 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 4/67...
mysql -u root -pmgsincos30 < choices_batch_004.sql
if %errorlevel% neq 0 (
    echo 选择批次 4 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 5/67...
mysql -u root -pmgsincos30 < choices_batch_005.sql
if %errorlevel% neq 0 (
    echo 选择批次 5 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 6/67...
mysql -u root -pmgsincos30 < choices_batch_006.sql
if %errorlevel% neq 0 (
    echo 选择批次 6 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 7/67...
mysql -u root -pmgsincos30 < choices_batch_007.sql
if %errorlevel% neq 0 (
    echo 选择批次 7 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 8/67...
mysql -u root -pmgsincos30 < choices_batch_008.sql
if %errorlevel% neq 0 (
    echo 选择批次 8 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 9/67...
mysql -u root -pmgsincos30 < choices_batch_009.sql
if %errorlevel% neq 0 (
    echo 选择批次 9 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 10/67...
mysql -u root -pmgsincos30 < choices_batch_010.sql
if %errorlevel% neq 0 (
    echo 选择批次 10 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 11/67...
mysql -u root -pmgsincos30 < choices_batch_011.sql
if %errorlevel% neq 0 (
    echo 选择批次 11 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 12/67...
mysql -u root -pmgsincos30 < choices_batch_012.sql
if %errorlevel% neq 0 (
    echo 选择批次 12 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 13/67...
mysql -u root -pmgsincos30 < choices_batch_013.sql
if %errorlevel% neq 0 (
    echo 选择批次 13 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 14/67...
mysql -u root -pmgsincos30 < choices_batch_014.sql
if %errorlevel% neq 0 (
    echo 选择批次 14 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 15/67...
mysql -u root -pmgsincos30 < choices_batch_015.sql
if %errorlevel% neq 0 (
    echo 选择批次 15 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 16/67...
mysql -u root -pmgsincos30 < choices_batch_016.sql
if %errorlevel% neq 0 (
    echo 选择批次 16 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 17/67...
mysql -u root -pmgsincos30 < choices_batch_017.sql
if %errorlevel% neq 0 (
    echo 选择批次 17 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 18/67...
mysql -u root -pmgsincos30 < choices_batch_018.sql
if %errorlevel% neq 0 (
    echo 选择批次 18 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 19/67...
mysql -u root -pmgsincos30 < choices_batch_019.sql
if %errorlevel% neq 0 (
    echo 选择批次 19 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 20/67...
mysql -u root -pmgsincos30 < choices_batch_020.sql
if %errorlevel% neq 0 (
    echo 选择批次 20 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 21/67...
mysql -u root -pmgsincos30 < choices_batch_021.sql
if %errorlevel% neq 0 (
    echo 选择批次 21 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 22/67...
mysql -u root -pmgsincos30 < choices_batch_022.sql
if %errorlevel% neq 0 (
    echo 选择批次 22 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 23/67...
mysql -u root -pmgsincos30 < choices_batch_023.sql
if %errorlevel% neq 0 (
    echo 选择批次 23 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 24/67...
mysql -u root -pmgsincos30 < choices_batch_024.sql
if %errorlevel% neq 0 (
    echo 选择批次 24 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 25/67...
mysql -u root -pmgsincos30 < choices_batch_025.sql
if %errorlevel% neq 0 (
    echo 选择批次 25 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 26/67...
mysql -u root -pmgsincos30 < choices_batch_026.sql
if %errorlevel% neq 0 (
    echo 选择批次 26 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 27/67...
mysql -u root -pmgsincos30 < choices_batch_027.sql
if %errorlevel% neq 0 (
    echo 选择批次 27 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 28/67...
mysql -u root -pmgsincos30 < choices_batch_028.sql
if %errorlevel% neq 0 (
    echo 选择批次 28 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 29/67...
mysql -u root -pmgsincos30 < choices_batch_029.sql
if %errorlevel% neq 0 (
    echo 选择批次 29 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 30/67...
mysql -u root -pmgsincos30 < choices_batch_030.sql
if %errorlevel% neq 0 (
    echo 选择批次 30 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 31/67...
mysql -u root -pmgsincos30 < choices_batch_031.sql
if %errorlevel% neq 0 (
    echo 选择批次 31 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 32/67...
mysql -u root -pmgsincos30 < choices_batch_032.sql
if %errorlevel% neq 0 (
    echo 选择批次 32 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 33/67...
mysql -u root -pmgsincos30 < choices_batch_033.sql
if %errorlevel% neq 0 (
    echo 选择批次 33 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 34/67...
mysql -u root -pmgsincos30 < choices_batch_034.sql
if %errorlevel% neq 0 (
    echo 选择批次 34 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 35/67...
mysql -u root -pmgsincos30 < choices_batch_035.sql
if %errorlevel% neq 0 (
    echo 选择批次 35 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 36/67...
mysql -u root -pmgsincos30 < choices_batch_036.sql
if %errorlevel% neq 0 (
    echo 选择批次 36 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 37/67...
mysql -u root -pmgsincos30 < choices_batch_037.sql
if %errorlevel% neq 0 (
    echo 选择批次 37 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 38/67...
mysql -u root -pmgsincos30 < choices_batch_038.sql
if %errorlevel% neq 0 (
    echo 选择批次 38 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 39/67...
mysql -u root -pmgsincos30 < choices_batch_039.sql
if %errorlevel% neq 0 (
    echo 选择批次 39 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 40/67...
mysql -u root -pmgsincos30 < choices_batch_040.sql
if %errorlevel% neq 0 (
    echo 选择批次 40 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 41/67...
mysql -u root -pmgsincos30 < choices_batch_041.sql
if %errorlevel% neq 0 (
    echo 选择批次 41 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 42/67...
mysql -u root -pmgsincos30 < choices_batch_042.sql
if %errorlevel% neq 0 (
    echo 选择批次 42 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 43/67...
mysql -u root -pmgsincos30 < choices_batch_043.sql
if %errorlevel% neq 0 (
    echo 选择批次 43 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 44/67...
mysql -u root -pmgsincos30 < choices_batch_044.sql
if %errorlevel% neq 0 (
    echo 选择批次 44 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 45/67...
mysql -u root -pmgsincos30 < choices_batch_045.sql
if %errorlevel% neq 0 (
    echo 选择批次 45 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 46/67...
mysql -u root -pmgsincos30 < choices_batch_046.sql
if %errorlevel% neq 0 (
    echo 选择批次 46 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 47/67...
mysql -u root -pmgsincos30 < choices_batch_047.sql
if %errorlevel% neq 0 (
    echo 选择批次 47 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 48/67...
mysql -u root -pmgsincos30 < choices_batch_048.sql
if %errorlevel% neq 0 (
    echo 选择批次 48 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 49/67...
mysql -u root -pmgsincos30 < choices_batch_049.sql
if %errorlevel% neq 0 (
    echo 选择批次 49 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 50/67...
mysql -u root -pmgsincos30 < choices_batch_050.sql
if %errorlevel% neq 0 (
    echo 选择批次 50 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 51/67...
mysql -u root -pmgsincos30 < choices_batch_051.sql
if %errorlevel% neq 0 (
    echo 选择批次 51 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 52/67...
mysql -u root -pmgsincos30 < choices_batch_052.sql
if %errorlevel% neq 0 (
    echo 选择批次 52 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 53/67...
mysql -u root -pmgsincos30 < choices_batch_053.sql
if %errorlevel% neq 0 (
    echo 选择批次 53 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 54/67...
mysql -u root -pmgsincos30 < choices_batch_054.sql
if %errorlevel% neq 0 (
    echo 选择批次 54 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 55/67...
mysql -u root -pmgsincos30 < choices_batch_055.sql
if %errorlevel% neq 0 (
    echo 选择批次 55 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 56/67...
mysql -u root -pmgsincos30 < choices_batch_056.sql
if %errorlevel% neq 0 (
    echo 选择批次 56 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 57/67...
mysql -u root -pmgsincos30 < choices_batch_057.sql
if %errorlevel% neq 0 (
    echo 选择批次 57 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 58/67...
mysql -u root -pmgsincos30 < choices_batch_058.sql
if %errorlevel% neq 0 (
    echo 选择批次 58 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 59/67...
mysql -u root -pmgsincos30 < choices_batch_059.sql
if %errorlevel% neq 0 (
    echo 选择批次 59 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 60/67...
mysql -u root -pmgsincos30 < choices_batch_060.sql
if %errorlevel% neq 0 (
    echo 选择批次 60 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 61/67...
mysql -u root -pmgsincos30 < choices_batch_061.sql
if %errorlevel% neq 0 (
    echo 选择批次 61 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 62/67...
mysql -u root -pmgsincos30 < choices_batch_062.sql
if %errorlevel% neq 0 (
    echo 选择批次 62 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 63/67...
mysql -u root -pmgsincos30 < choices_batch_063.sql
if %errorlevel% neq 0 (
    echo 选择批次 63 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 64/67...
mysql -u root -pmgsincos30 < choices_batch_064.sql
if %errorlevel% neq 0 (
    echo 选择批次 64 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 65/67...
mysql -u root -pmgsincos30 < choices_batch_065.sql
if %errorlevel% neq 0 (
    echo 选择批次 65 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 66/67...
mysql -u root -pmgsincos30 < choices_batch_066.sql
if %errorlevel% neq 0 (
    echo 选择批次 66 导入失败！
    pause
    exit /b 1
)

echo 导入选择批次 67/67...
mysql -u root -pmgsincos30 < choices_batch_067.sql
if %errorlevel% neq 0 (
    echo 选择批次 67 导入失败！
    pause
    exit /b 1
)

echo 所有数据导入完成！
pause
