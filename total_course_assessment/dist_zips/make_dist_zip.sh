#!/bin/bash

rm -f MacOS_CG_Score.zip
rm -rf MacOS_CG_Score
mkdir MacOS_CG_Score
cp -r ../dist/cg_score_gui.app MacOS_CG_Score/
zip -r MacOS_CG_Score.zip MacOS_CG_Score/
rm -rf MacOS_CG_Score
